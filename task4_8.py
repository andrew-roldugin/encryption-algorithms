import math
from sympy import primefactors, gcdex


def split(msg: int, n: int):
    l1 = len(str(n))
    msg = str(msg)
    l2 = len(msg)
    blocks = []
    l = math.ceil(l2 / l1)
    for i in range(l):
        b = msg[i * l1: (i + 1) * l1]
        if len(b) < l1:
            msg = msg.rjust(l1, '0')
        blocks.append(int(b))
    return blocks


def decrypt(C: int, d: int, n: int):
    blocks = split(C, n)
    res = ''
    for num in blocks:
        res += str(pow(num, d, n))
    s = [chr(int(res[i: i + 2])) for i in range(0, len(res), 2)]
    return ' '.join(s)


if __name__ == '__main__':
    n = 491372401012837
    e = 12791

    C = 360070592525747_235561760474154_397895457211297_337782333456643_132578626273135_63214958731488
    print('Зашифрованный текст:', C)

    p, q = primefactors(n)
    print('p =', p, ', q =', q)

    phi = (p - 1) * (q - 1)
    print('f =', phi)

    d = gcdex(e, phi)[0].p
    print('d =', d)

    P = decrypt(C, d, n)
    print('Расшифрованый текст:', P)
