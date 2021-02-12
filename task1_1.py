import os

from bitarray._bitarray import bitarray


def right_shift(array, n):
    res = bitarray(len(array))
    for i in range(len(array)):
        res[i] = array[i]
    for j in range(n):
        for i in reversed(range(1, len(array))):
            res[i] = array[i - 1]
        res[0] = 0
        array = res
    return res


def left_shift(array, n):
    res = bitarray(len(array))
    for i in range(len(array)):
        res[i] = array[i]
    for j in range(n):
        for i in range(len(array) - 1):
            res[i] = array[i + 1]
        res[-1] = 0
        array = res
    return res



def bytestring2bitarray(input_string):
    bits_input_string = bitarray()
    for char in input_string:
        aa = ''.join(['0'] * (8 - len(bin(char)[2:])))
        bits_input_string += aa + bin(char)[2:]
    return bits_input_string


def F(left, key):
    return left_shift(left, 9) ^ (~(right_shift(key, 11) & left))


def get_K_i(K, i):
    return right_shift(K, i * 8)[:32]


def encrypt(plaintext, key, size_block=64, n=2):
    for i in range(n):
        res = bitarray()
        k_i = get_K_i(key, i)
        for index_of_block in range(len(plaintext) // 64):
            block = plaintext[size_block * index_of_block: size_block * (index_of_block + 1)]
            left = block[0:size_block // 2]
            right = block[size_block // 2: size_block]
            temp = F(left, k_i) ^ right
            #new_block = right + temp
            new_block = temp + left
            res += new_block
        plaintext = res
    return res

def decrypt(plaintext, key, size_block=64, n=2):
    for i in range(n):
        res = bitarray()
        k_i = get_K_i(key, n - i - 1)
        for index_of_block in range(len(plaintext) // 64):
            block = plaintext[size_block * index_of_block: size_block * (index_of_block + 1)]
            left = block[0:size_block // 2]
            right = block[size_block // 2: size_block]
            temp = F(left, k_i) ^ right
            #new_block = right + temp
            new_block = temp + left
            res += new_block
        plaintext = res
    return res


input_string = b'Very very secret text'
input_string = bytes([0] * (8 - len(input_string) % 8)) + input_string
binput_string = bytestring2bitarray(input_string)
#key = bytearray(os.urandom(8))
bkey = bitarray('1') * 64
#bkey = bytestring2bitarray(key)
print('исходн:', binput_string)
print('_ключ_:', bkey)
print('зашфрв:', encrypt(binput_string, bkey))
print('расшфр:', decrypt(encrypt(binput_string, bkey), bkey))