from Crypto.Util.number import inverse


def factor(num):
    result = []
    d = 2
    while d * d <= num:
        if num % d == 0:
            result.append(d)
            num //= d
        else:
            d += 1
    if num > 1:
        result.append(num)
    return result


def blocking(num, size_num, size_block):
    return [int.from_bytes(num.to_bytes(size_num, 'big')[i * size_block: (i + 1) * size_block], 'big') for i in
            range(size_num // size_block)]


def decrypt(C, d, n):
    bytes_val = blocking(C, 32, 4)
    res = bytearray()
    for num in bytes_val:
        res += pow(num, d, n).to_bytes(8, 'big')
    return int.from_bytes(res, 'big')


def encrypt(P, e, n):
    bytes_val = blocking(P, 64, 8)

    res = bytearray()
    for num in bytes_val:
        res += pow(num, e, n).to_bytes(4, 'big')
    return int.from_bytes(res, 'big')


n = 471090785117207
e = 12377

C = 314999112281065205361706341517321987491098667

print('Зашифрованный текст:', C)

p, q = factor(n)
print('p =', p, ', q =', q)
f = (p - 1) * (q - 1)
print('f =', f)

d = inverse(e, f)

print('d =', d)

P = decrypt(C, d, n)

print('Расшифрованый текст:', P)

C = encrypt(P, e, n)
print('<Проверка> Зашифрованный текст:', C)
