import os

from bitarray._bitarray import bitarray


def xor(a, b):
    res = bytearray([0] * len(a))
    for i in range(len(a)):
        res[i] = a[i] ^ b[i]
    return res


def no(a):
    res = bytearray([0] * len(a))
    for i in range(len(a)):
        res[i] = 255 - a[i]
    return res


def right_shift(array, n):
    return (int.from_bytes(array, 'big') >> n).to_bytes(8, 'big')[0:4]


def left_shift(array, n):
    return (int.from_bytes(array, 'big') << n).to_bytes(8, 'big')[0:4]


def or_arr(a, b):
    res = bytearray([0] * len(a))
    for i in range(len(a)):
        res[i] = a[i] & b[i]
    return res


def F(left, key):
    return xor((left_shift(left, 9)), no(or_arr((right_shift(key, 11)), left)))


def get_K_i(K, i):
    return right_shift(K, i * 8)[0:32]


def encrypt(plaintext, key, size_block=8, n=2):
    for j in range(n):
        res = b''
        for i in range(len(plaintext) // 8):
            block = plaintext[size_block * i: size_block * (i + 1)]
            left = block[0:size_block // 2]
            right = block[size_block // 2: size_block]
            k_i = get_K_i(key, j)
            temp = xor(F(left, k_i), right)
            new_block = right + temp
            res += new_block
        plaintext = res
    return res


def decrypt(plaintext, key, size_block=8, n=2):
    for j in range(n):
        res = b''
        for i in range(len(plaintext) // 8):
            block = plaintext[size_block * i: size_block * (i + 1)]
            left = block[0:size_block // 2]
            right = block[size_block // 2: size_block]
            k_i = get_K_i(key, n - j - 1)
            temp = xor(F(left, k_i), right)
            new_block = right + temp
            res += new_block
        plaintext = res
    return res


input_string = b'Very very secret text'
key = bytearray(os.urandom(6))
block = 64
input_string += bytes([0] * (8 - len(input_string) % 8))
L = block / 2
R = block / 2
array = bytearray(input_string)
b = 6
aaa = bitarray(64)
print(decrypt(encrypt(input_string, key), key))
