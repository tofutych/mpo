import numpy
import numpy as np
import numdifftools as nd


def makeData():
    # Строим сетку в интервале от -10 до 10, имеющую 100 отсчетов по обоим координатам
    x = numpy.linspace(-10, 10, 100)
    y = numpy.linspace(-10, 10, 100)

    # Создаем двумерную матрицу-сетку
    xgrid, ygrid = numpy.meshgrid(x, y)

    # В узлах рассчитываем значение функции
    z = numpy.power((numpy.power(xgrid, 2) + ygrid - 11), 2) + numpy.power(
        (xgrid + numpy.power(ygrid, 2) - 7), 2
    )
    return xgrid, ygrid, z


def Funct_consider(res_x, res_y, res_step, res_iterations):
    himmelblaus_function = lambda x, y: numpy.power(
        (numpy.power(x, 2) + y - 11), 2
    ) + numpy.power((x + numpy.power(y, 2) - 7), 2)

    x_list = []
    y_list = []
    z_list = []

    # Строим сетку в интервале от -10 до 10, имеющую 100 отсчетов по обоим координатам
    for item in gradient_descent(
        himmelblaus_function, res_x, res_y, res_step, res_iterations
    ):
        x_list.append(item[0])
        y_list.append(item[1])
        z_list.append(item[3])

    return x_list, y_list, z_list


def partial_function(f___, input, pos, value):
    tmp = input[pos]
    input[pos] = value
    ret = f___(*input)
    input[pos] = tmp
    return ret


def gradient(function, input):
    """Частная произвоздная по каждому из параметров функции f(т.е. градиент)"""

    ret = np.empty(len(input))
    for i in range(len(input)):
        fg = lambda x: partial_function(function, input, i, x)
        ret[i] = nd.Derivative(fg)(input[i])
    return ret


def next_point(x, y, gx, gy, step) -> tuple:
    return x - step * gx, y - step * gy


def gradient_descent(function, x0, y0, tk, M):
    yield x0, y0, 0, function(x0, y0)

    e1 = 0.0001
    e2 = 0.0001

    k = 0
    while True:
        (gx, gy) = gradient(function, [x0, y0])  # Шаг 3

        if (
            np.linalg.norm((gx, gy)) < e1
        ):  # Шаг 4. Проверить выполнение критерия окончания
            break

        if k >= M:  # Шаг 5
            break

        x1, y1 = next_point(x0, y0, gx, gy, tk)  # Шаг 7
        f1 = function(x1, y1)
        f0 = function(x0, y0)
        while not f1 < f0:  # Шаг 8
            tk = tk / 2
            x1, y1 = next_point(x0, y0, gx, gy, tk)
            f1 = function(x1, y1)
            f0 = function(x0, y0)

        if np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) < e2 and abs(f1 - f0) < e2:  # Шаг 9
            x0, y0 = x1, y1
            break
        else:
            k += 1
            x0, y0 = x1, y1
            yield x0, y0, k, f1
