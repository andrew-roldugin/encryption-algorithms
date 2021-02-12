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


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


n = 471090785117207
e = 12377

C = 314999112281065205361706341517321987491098667

p, q = factor(n)
print('p =', p, ', q =', q)
f = (p - 1) * (q - 1)
d = inverse(e, f)
print('d =', d)

P = pow(C, d, n)
print(P)

# TODO: непонятно почему не совпадает зашифрованной вновь текст. Нужно найти проблему
print(pow(P, e, n))
