# -*- coding: utf-8 -*-
import math
import random

from labs.services import pybee


class spherebee(pybee.floatbee):
    """Функция - сумма квадратов по каждой координате"""

    # Количество координат
    count = 4

    @staticmethod
    def getstartrange():
        return [150.0] * spherebee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * spherebee.count

    def __init__(self):
        pybee.floatbee.__init__(self)

        self.minval = [-150.0] * spherebee.count
        self.maxval = [150.0] * spherebee.count

        self.position = [random.uniform(
            self.minval[n], self.maxval[n]) for n in range(spherebee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
        self.fitness = 0.0
        for val in self.position:
            self.fitness -= val * val


###################################################

class dejongbee(pybee.floatbee):
    """Функция De Jong"""

    # Количество координат
    count = 2

    @staticmethod
    def getstartrange():
        return [2.048] * dejongbee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * dejongbee.count

    def __init__(self):
        pybee.floatbee.__init__(self)

        self.minval = [-2.048] * dejongbee.count
        self.maxval = [2.048] * dejongbee.count

        self.position = [random.uniform(
            self.minval[n], self.maxval[n]) for n in range(dejongbee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
        x1 = self.position[0]
        x2 = self.position[1]

        self.fitness = 3905.93 - 100.0 * \
            ((x1 * x1 - x2) ** 2) - ((1 - x1) ** 2)


###################################################

class goldsteinbee(pybee.floatbee):
    """Функция Goldstein & Price"""

    # Количество координат
    count = 2

    @staticmethod
    def getstartrange():
        return [2.0] * goldsteinbee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * goldsteinbee.count

    def __init__(self):
        pybee.floatbee.__init__(self)

        self.minval = [-2.0] * goldsteinbee.count
        self.maxval = [2.0] * goldsteinbee.count

        self.position = [random.uniform(
            self.minval[n], self.maxval[n]) for n in range(goldsteinbee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
        x1 = self.position[0]
        x2 = self.position[1]

        self.fitness = -(1.0 + ((x1 + x2 + 1.0) ** 2) *
                         (19.0 - 14.0 * x1 + 3.0 * x1 * x1 - 14.0 * x2 + 6.0 * x1 * x2 + 3.0 * x2 * x2)) * \
            (30.0 + ((2.0 * x1 - 3.0 * x2) ** 2) *
             (18.0 - 32.0 * x1 + 12.0 * x1 * x1 + 48.0 * x2 - 36.0 * x1 * x2 + 27.0 * x2 * x2))


###################################################

class rosenbrockbee(pybee.floatbee):
    """Функция Rosenbrock"""

    # Количество координат
    count = 4

    @staticmethod
    def getstartrange():
        return [10.0] * rosenbrockbee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * rosenbrockbee.count

    def __init__(self):
        pybee.floatbee.__init__(self)

        self.minval = [-10.0] * rosenbrockbee.count
        self.maxval = [10.0] * rosenbrockbee.count

        self.position = [random.uniform(
            self.minval[n], self.maxval[n]) for n in range(rosenbrockbee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""

        self.fitness = 0.0
        for n in range(3):
            xi = self.position[n]
            xi1 = self.position[n + 1]

            self.fitness -= 100.0 * (((xi * xi - xi1) ** 2) + ((1 - xi) ** 2))


###################################################

class testbee(pybee.floatbee):
    count = 4

    @staticmethod
    def getstartrange():
        return [20.0] * testbee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * testbee.count

    """Функция	из статьи"""

    def __init__(self):
        pybee.floatbee.__init__(self)

        self.minval = [-500.0] * testbee.count
        self.maxval = [500.0] * testbee.count

        self.position = [random.uniform(
            self.minval[n], self.maxval[n]) for n in range(testbee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""

        self.fitness = 0.0
        for n in range(testbee.count):
            xi = self.position[n]

            self.fitness += -xi * math.sin(math.sqrt(abs(xi)))

        self.fitness *= -1


###################################################

class funcbee(pybee.floatbee):
    """Пчела для поиска коэффициентов степенной функции"""

    # Количество координат
    count = 5

    @staticmethod
    def getstartrange():
        return [5.0] * funcbee.count

    @staticmethod
    def getrangekoeff():
        return [0.995, 0.99, 0.97, 0.95, 0.9]

    def __init__(self):
        pybee.floatbee.__init__(self)

        # Количество точек для расчета
        self.xcount = 30

        self.minval = [-15.0] * funcbee.count
        self.maxval = [15.0] * funcbee.count

        # Интервал, в котором могут изменяться значения x (не координаты пчелы)
        xmin = -20.0
        xmax = 20.0

        # Точки для расчета целевой функции. У каждой пчелы задается случайным образом
        self.x1_points = [random.uniform(xmin, xmax)
                          for n in range(self.xcount)]
        self.x2_points = [random.uniform(xmin, xmax)
                          for n in range(self.xcount)]
        self.x3_points = [random.uniform(xmin, xmax)
                          for n in range(self.xcount)]
        self.x4_points = [random.uniform(xmin, xmax)
                          for n in range(self.xcount)]

        # Рассчитаем значения правильной целевой функции
        self.correct_vals = [
            self.correctfunc(
                self.x1_points[n], self.x2_points[n], self.x3_points[n], self.x4_points[n])
            for n in range(self.xcount)]

        self.position = [random.uniform(
            self.minval[n], self.maxval[n]) for n in range(funcbee.count)]
        self.calcfitness()

    def correctfunc(self, x1, x2, x3, x4):
        """Правильная целевая функция"""
        a4 = 10.01
        a3 = 1.72
        a2 = -5.93
        a1 = 9.94
        a0 = -13.55

        return a4 * (x4 ** 4) + a3 * (x3 ** 3) + a2 * (x2 ** 2) + a1 * x1 + a0

    def unknownfunc(self, x1, x2, x3, x4):
        return self.position[4] * (x4 ** 4) + \
            self.position[3] * (x3 ** 3) + \
            self.position[2] * (x2 ** 2) + \
            self.position[1] * x1 + \
            self.position[0]

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""

        self.fitness = 0.0
        for n in range(self.xcount):
            self.fitness -= \
                abs(self.unknownfunc(self.x1_points[n], self.x2_points[n], self.x3_points[n], self.x4_points[n]) -
                    self.correct_vals[n])

        self.fitness /= self.xcount

###################################################
