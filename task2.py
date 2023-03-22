import math
import os

from bitarray._bitarray import bitarray
from bitarray.util import ba2int, ba2hex


def right_shift(block, n):
    b = block if block.__class__ is bitarray else bitarray(block)
    return b >> n


def left_shift(block, n):
    b = block if block.__class__ is bitarray else bitarray(block)
    return b << n


def F(left, key):
    return left_shift(left, 9) ^ (~(right_shift(key, 11) & left))


def preprocess(arr):
    ba = bitarray(endian='big')
    ba.frombytes(arr)
    return ba


class Cipher:
    def __init__(self, key, rounds=8, block_size=64):
        self.block_size = block_size
        self.rounds = rounds

        ba = bitarray(endian='big')

        self.key = key
        ba.frombytes(self.key)
        self.bkey = ba

    def key(self):
        return ba2int(self.bkey).to_bytes(self.bkey.nbytes, 'big').decode()

    def align(self, s):
        return s.ljust(math.ceil(math.ceil(8 * len(s) / self.block_size) * self.block_size / 8), b'\0')

    def get_partitions(self, msg):
        for i in range(len(msg) // self.block_size):
            yield msg[self.block_size * i: self.block_size * (i + 1)]

    def split_block(self, block, branches=2):
        border = self.block_size // branches
        return [block[border * i: border * (i + 1)] for i in range(branches)]

    def get_Ki(self, key, i, num_branches):
        return right_shift(key, i * 4)[:(self.block_size // num_branches)]

    def encrypt(self, message):
        msg = preprocess(self.align(message))
        res = bitarray()
        for block in self.get_partitions(msg):
            res += self.encrypt_block(block)

        return res

    def encrypt_block(self, block):
        x1, x2, x3, x4 = self.split_block(block, 4)
        for i in range(self.rounds):
            k_i = self.get_Ki(self.bkey, i, 4)

            f = F(x1, k_i)
            if i == self.rounds - 1:
                x1 = x1
                x2 = f ^ x2
                x3 = f ^ x3
                x4 = f ^ x4
            else:
                x1_ = x1.copy()
                x1 = f ^ x2
                x2 = f ^ x3
                x3 = f ^ x4
                x4 = x1_

        return x1 + x2 + x3 + x4

    def decrypt(self, message: bitarray):
        msg = message
        res = bitarray()
        for block in self.get_partitions(msg):
            res += self.decrypt_block(block)
        return res

    def decrypt_block(self, block):
        x1, x2, x3, x4 = self.split_block(block, 4)
        for i in reversed(range(self.rounds)):
            k_i = self.get_Ki(self.bkey, i, 4)

            f = F(x1, k_i)
            if i == 0:
                x1 = x1
                x2 = f ^ x2
                x3 = f ^ x3
                x4 = f ^ x4
            else:
                x1_ = x1.copy()
                x1 = f ^ x4
                x4 = f ^ x3
                x3 = f ^ x2
                x2 = x1_

        return x1 + x2 + x3 + x4

    def encrypt_CBC(self, message, IV):
        res = bitarray()
        for i, block in enumerate(self.get_partitions(preprocess(self.align(message)))):
            if i == 0:
                block ^= IV
            else:
                block ^= res[self.block_size * (i - 1): self.block_size * i]
            res += self.encrypt_block(block)
        return res

    def decrypt_CBC(self, ba, IV):
        res = bitarray()
        for i, block in enumerate(self.get_partitions(ba)):
            decrypted_block = self.decrypt_block(block)
            if i == 0:
                decrypted_block ^= IV
            else:
                decrypted_block ^= ba[self.block_size * (i - 1): self.block_size * i]

            res += decrypted_block
        return res

    def encrypt_CFB(self, message, IV):
        message = preprocess(self.align(message))
        res = bitarray()
        for i, block in enumerate(self.get_partitions(message)):
            if i == 0:
                decrypted_block = self.encrypt_block(IV) ^ block
            else:
                decrypted_block = self.encrypt_block(res[self.block_size * (i - 1): self.block_size * i]) ^ block

            res += decrypted_block
        return res

    def decrypt_CFB(self, ba, IV):
        res = bitarray()
        for i, block in enumerate(self.get_partitions(ba)):
            if i == 0:
                decrypted_block = self.encrypt_block(IV) ^ block
            else:
                decrypted_block = self.encrypt_block(ba[self.block_size * (i - 1): self.block_size * i]) ^ block

            res += decrypted_block
        return res


if __name__ == '__main__':
    input_string = bytes('Самый главный секрет ФКНа', 'utf8')

    c = Cipher(key=os.urandom(8), block_size=64, rounds=10)
    C = c.encrypt(input_string)
    M = c.decrypt(C.copy())

    t = preprocess(input_string)
    print('Исходное сообщение: {1}'.format(input_string, ba2hex(t)))
    print('Ключ К: {}'.format(ba2hex(c.bkey)))
    print('Зашифрованное сообщение: {1}'.format(ba2int(C).to_bytes(C.nbytes, 'big').decode('latin1'), ba2hex(C)))
    print('Расшифрованное сообщение: {0} = {1}'.format(ba2int(M).to_bytes(M.nbytes, 'big')[:len(input_string)].decode(),
                                                       ba2hex(M)))

    ba = bitarray(endian='big')
    ba.frombytes(os.urandom(8))
    IV = ba

    print('-------------------CBC----------------')
    C_CBC = c.encrypt_CBC(input_string, IV)
    M_CBC = c.decrypt_CBC(C_CBC, IV)

    print('Исходное сообщение: {1}'.format(input_string, ba2hex(t)))
    print('Ключ К: {}'.format(ba2hex(c.bkey)))
    print('Зашифрованное сообщение: {1}'.format(ba2int(C_CBC).to_bytes(C_CBC.nbytes, 'big').decode('latin1'),
                                                ba2hex(C_CBC)))
    print('Расшифрованное сообщение: {0} = {1}'.format(
        ba2int(M_CBC).to_bytes(M_CBC.nbytes, 'big')[:len(input_string)].decode(),
        ba2hex(M_CBC)))

    print('-------------------CFB----------------')
    C_CFB = c.encrypt_CFB(input_string, IV)
    M_CFB = c.decrypt_CFB(C_CFB, IV)

    print('Зашифрованное сообщение: {1}'.format(ba2int(C_CFB).to_bytes(C_CFB.nbytes, 'big').decode('latin1'),
                                                ba2hex(C_CFB)))
    print('Расшифрованное сообщение: {0} = {1}'.format(
        ba2int(M_CFB).to_bytes(M_CFB.nbytes, 'big')[:len(input_string)].decode(),
        ba2hex(M_CFB)))
