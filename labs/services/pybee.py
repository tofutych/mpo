# -*- coding: utf-8 -*-
"""
Реализация алгоритма роя пчел
"""

import math
import random


class floatbee:
    """Класс пчел, где в качестве координат используется список дробных чисел"""

    def __init__(self):
        # Положение пчелы (искомые величины)
        self.position = None

        # Интервалы изменений искомых величин (координат)
        self.minval = None
        self.maxval = None

        # Значение целевой функции
        self.fitness = 0.0

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
        pass

    def sort(self, otherbee):
        """Функция для сортировки пчел по их целевой функции (здоровью) в порядке убывания."""
        if self.fitness < otherbee.fitness:
            return -1
        elif self.fitness > otherbee.fitness:
            return 1
        else:
            return 0

    def otherpatch(self, bee_list, range_list):
        """Проверить находится ли пчела на том же участке, что и одна из пчел в bee_list.
        range_list - интервал изменения каждой из координат"""
        if len(bee_list) == 0:
            return True

        for curr_bee in bee_list:
            position = curr_bee.getposition()

            for n in range(len(self.position)):
                if abs(self.position[n] - position[n]) > range_list[n]:
                    return True

        return False

    def getposition(self):
        """Вернуть копию (!) своих координат"""
        return [val for val in self.position]

    def goto(self, otherpos, range_list):
        """Перелет в окрестность места, которое нашла другая пчела. Не в то же самое место! """

        # К каждой из координат добавляем случайное значение
        self.position = [otherpos[n] + random.uniform(-range_list[n], range_list[n])
                         for n in range(len(otherpos))]

        # Проверим, чтобы не выйти за заданные пределы
        self.checkposition()

        # Расчитаем и сохраним целевую функцию
        self.calcfitness()

    def gotorandom(self):
        # Заполним координаты случайными значениями
        self.position = [random.uniform(
            self.minval[n], self.maxval[n]) for n in range(len(self.position))]
        self.checkposition()
        self.calcfitness()

    def checkposition(self):
        """Скорректировать координаты пчелы, если они выходят за установленные пределы"""
        for n in range(len(self.position)):
            if self.position[n] < self.minval[n]:
                self.position[n] = self.minval[n]

            elif self.position[n] > self.maxval[n]:
                self.position[n] = self.maxval[n]


class hive:
    """Улей. Управляет пчелами"""

    def __init__(self, scoutbeecount, selectedbeecount, bestbeecount,
                 selsitescount, bestsitescount,
                 range_list, beetype):
        """scoutbeecount - Количество пчел-разведчиков
        selectedbeecount - количество пчел, посылаемое на один из лучших участков
        selectedbeecount - количество пчел, посылаемое на остальные выбранные участки

        selsitescount - количество выбранных участков
        bestsitescount - количество лучших участков среди выбранных
        beetype - класс пчелы, производный от bee

        range_list - список диапазонов координат для одного участка"""

        self.scoutbeecount = scoutbeecount
        self.selectedbeecount = selectedbeecount
        self.bestbeecount = bestbeecount

        self.selsitescount = selsitescount
        self.bestsitescount = bestsitescount

        self.beetype = beetype

        self.range = range_list

        # Лучшая на данный момент позиция
        self.bestposition = None

        # Лучшее на данный момент здоровье пчелы (чем больше, тем лучше)
        self.bestfitness = -1.0e9

        # Начальное заполнение роя пчелами со случайными координатами
        beecount = scoutbeecount + selectedbeecount * \
            selsitescount + bestbeecount * bestsitescount
        self.swarm = [beetype() for n in range(beecount)]

        # Лучшие и выбранные места
        self.bestsites = []
        self.selsites = []

        self.swarm.sort(floatbee.sort, reverse=True)
        self.bestposition = self.swarm[0].getposition()
        self.bestfitness = self.swarm[0].fitness

    def sendbees(self, position, index, count):
        """ Послать пчел на позицию.
        Возвращает номер следующей пчелы для вылета """
        for n in range(count):
            # Чтобы не выйти за пределы улея
            if index == len(self.swarm):
                break

            curr_bee = self.swarm[index]

            if curr_bee not in self.bestsites and curr_bee not in self.selsites:
                # Пчела не на лучших или выбранных позициях
                curr_bee.goto(position, self.range)

            index += 1

        return index

    def nextstep(self):
        """Новая итерация"""
        # Выбираем самые лучшие места и сохраняем ссылки на тех, кто их нашел
        self.bestsites = [self.swarm[0]]

        curr_index = 1
        for currbee in self.swarm[curr_index: -1]:
            # Если пчела находится в пределах уже отмеченного лучшего участка, то ее положение не считаем
            if currbee.otherpatch(self.bestsites, self.range):
                self.bestsites.append(currbee)

                if len(self.bestsites) == self.bestsitescount:
                    break

            curr_index += 1

        self.selsites = []

        for currbee in self.swarm[curr_index: -1]:
            if currbee.otherpatch(self.bestsites, self.range) and currbee.otherpatch(self.selsites, self.range):
                self.selsites.append(currbee)

                if len(self.selsites) == self.selsitescount:
                    break

        # Отправляем пчел на задание :)
        # Отправляем сначала на лучшие места

        # Номер очередной отправляемой пчелы. 0-ую пчелу никуда не отправляем
        bee_index = 1

        for best_bee in self.bestsites:
            bee_index = self.sendbees(
                best_bee.getposition(), bee_index, self.bestbeecount)

        for sel_bee in self.selsites:
            bee_index = self.sendbees(
                sel_bee.getposition(), bee_index, self.selectedbeecount)

        # Оставшихся пчел пошлем куда попадет
        for curr_bee in self.swarm[bee_index: -1]:
            curr_bee.gotorandom()

        self.swarm.sort(floatbee, reverse=True)
        self.bestposition = self.swarm[0].getposition()
        self.bestfitness = self.swarm[0].fitness


class statistic:
    """ Класс для сбора статистики по запускам алгоритма"""

    def __init__(self):
        # Индекс каждого списка соответствует итерации.
        # В  элементе каждого списка хранится список значений для каждого запуска
        # Добавлять надо каждую итерацию

        # Значения целевой функции в зависимости от номера итерации
        self.fitness = []

        # Значения координат в зависимости от итерации
        self.positions = []

        # Размеры областей для поискарешения в зависимости от итерации
        self.range = []

    def add(self, runnumber, currhive):
        range_vals = [val for val in currhive.range]
        fitness = currhive.bestfitness
        positions = currhive.swarm[0].getposition()

        assert (len(self.positions) == len(self.fitness))
        assert (len(self.range) == len(self.fitness))

        if runnumber == len(self.fitness):
            self.fitness.append([fitness])
            self.positions.append([positions])
            self.range.append([range_vals])
        else:
            assert (runnumber == len(self.fitness) - 1)

            self.fitness[runnumber].append(fitness)
            self.positions[runnumber].append(positions)
            self.range[runnumber].append(range_vals)

    def formatfitness(self, runnumber):
        """Сформировать таблицу целевой функции"""
        result = ""
        for n in range(len(self.fitness[runnumber])):
            line = "%6.6d    %10f\n" % (n, self.fitness[runnumber][n])
            result += line

        return result

    def formatcolumns(self, runnumber, column):
        """Форматировать список списков items для вывода"""
        result = ""

        for n in range(len(column[runnumber])):
            line = "%6.6d" % n

            for val in column[runnumber][n]:
                line += "    %10f" % val

            line += "\n"
            result += line

        return result

    def formatpos(self, runnumber):
        return self.formatcolumns(runnumber, self.positions)

    def formatrange(self, runnumber):
        return self.formatcolumns(runnumber, self.range)
