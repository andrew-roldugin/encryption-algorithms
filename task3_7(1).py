import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from statistics import NormalDist

flag = True


def _generate(R, z, n):
    z: float = z + 10 ** (-n)
    temp: float = R / z + math.pi
    return temp - temp.__trunc__(), z


def get_random_array(length, z0=0, r0=0.73, n=4):
    z = [z0]
    R = [r0]
    R_uniq = {r0: 0}
    L = -1  # длина апериодичности
    l = -1  # длина повторяющейся подпоследовательности

    def _inner_(R_uniq, r_new):
        nonlocal L, l
        L = len(R_uniq)
        l = L - R_uniq[r_new]

    for i in range(length - 1):
        r_new, z_new = _generate(R[-1], z[-1], n)
        z.append(z_new)
        if r_new in R_uniq:
            _inner_(R_uniq, r_new)
            break
        else:
            R_uniq[r_new] = i
            R.append(r_new)

    if L == -1:
        _inner_(R_uniq, r0)

    return R, L, l


def test6(R, N):
    c = 0
    for i in range(0, N - 1, 2):
        val = math.hypot(R[i], R[i + 1])
        if val < 1:
            c += 1
    return 8 * c / N


if __name__ == '__main__':
    alpha = 0.99  # уровень значимости
    delta = 0.01  # доверительный интервал (здесь 5%)
    N = int((NormalDist().inv_cdf((1 - alpha) / 2) / (2 * delta)) ** 2)

    print('------------------------------------ Результаты работы программы ------------------------------------')
    X, Y, Z = np.empty((10, 10)), np.empty((10, 10)), np.empty((10, 10))

    for run in range(0, 10):
        for i, r0 in enumerate(np.linspace(0, 1, 10, endpoint=False)):
            X[run, i] = r0

            for j, z0 in enumerate(np.linspace(0, 1, 10, endpoint=False)):
                R, L, l = get_random_array(length=N, z0=z0, r0=r0, n=run + 15)
                print(f'z0={z0}; r0 ={r0}')

                print(
                    '\tНаибольшая длина неповторяющихся элементов: {}\nдлина повторяющейся подпоследовательности: {}'.format(
                        L, l))

                pi_ = test6(R, L)
                Y[run, j] = z0
                Z[run, i] = pi_
                print(pi_)

    # X = X.repeat(10).reshape(10, 10)
    # Y = Y.repeat(10).reshape(10, 10)
    # Z = Z.repeat(10).reshape(10, 10)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(X, Y, Z)
    P = np.empty((10, 10))
    P.fill(math.pi)
    ax.plot_surface(X, Y, P)
    plt.show()
    # sns_plot = sns.distplot(R)
    # fig = sns_plot.get_figure()
    # plt.show()
    #
    # x = [R[2 * i] for i in range(len(R) // 2)]
    # y = [R[2 * i + 1] for i in range(len(R) // 2)]
    #
    # hist, x_edges, y_edges = np.histogram2d(x, y, bins=10)
    #
    # plt.imshow(hist, extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]])
    # plt.xticks(ticks=x_edges)
    # plt.xlabel('x')
    # plt.yticks(ticks=y_edges)
    # plt.ylabel('y')
    # plt.show()
