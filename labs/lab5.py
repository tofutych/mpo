import time
import tkinter
from tkinter import *

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def Lab_5_window():
    # Определить оптимизируемую функцию: она может обрабатывать только один вход в виде вектора строки, если существует несколько входов в виде матрицы, выполнить итерацию
    def CostFunction(input):
        x = input[0]
        y = input[1]
        result = (x ** 2 - 10 * np.cos(2 * np.pi * x)) + \
            (y ** 2 - 10 * np.cos(2 * np.pi * y)) + 20
        return result

    def get_rastrigin_surface():
        X = np.linspace(-4, 4, 200)
        Y = np.linspace(-4, 4, 200)

        X, Y = np.meshgrid(X, Y)

        Z = CostFunction([X, Y])
        return X, Y, Z
    # Инициализировать параметры

    def draw():
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(X, Y, Z, rstride=10, cstride=10,
                        alpha=0.4, cmap="seismic")
        canvas.draw()
        Npop = txt_1.get()
        Nloc = txt_2.get()
        A = txt_3.get()
        maxIter = txt_4.get()
        pn = bee(int(Npop), int(Nloc), int(A), int(maxIter))

        for i in range(0, int(maxIter)):
            value = CostFunction([pn[i][0], pn[i][1]])
            if i != int(maxIter) - 1:
                ax.scatter(pn[i][0], pn[i][1], value, c="black", s=3)
                print(
                    f"Значение функции = {value} в точке x = {pn[i][0]}, y = {pn[i][1]}\n")
            else:
                ax.scatter(pn[i][0], pn[i][1], value, c="red", s=10)
                print(
                    f'Наименьшее значение функции = {value} в точке x={pn[i][0]}, y={pn[i][1]}')
                break
            canvas.draw()
            window_lab_5.update()
            delay = txt_5.get()
            time.sleep(float(delay))

    def bee(Npop, Nloc, A, maxIter):

        # Число и диапазон параметров в функции стоимости
        nVar = 2
        VarMin = -4
        VarMax = 4

        # Основные параметры алгоритма роя
        iter_max = maxIter
        nPop = Npop
        nOnLooker = Nloc
        L = np.around(0.6*float(nVar)*float(nPop))
        a = A

        # Создать каждую матрицу записи
        PopPosition = np.zeros([nPop, nVar])
        PopCost = np.zeros([nPop, 1])
        Probability = np.zeros([nPop, 1])
        BestSol = np.zeros([iter_max+1, nVar])
        BestCost = np.inf*np.ones([iter_max+1, 1])
        Mine = np.zeros([nPop, 1])

        # Инициализировать местоположение источника меда
        PopPosition = 8*np.random.rand(nPop, nVar) - 4
        for i in range(nPop):
            PopCost[i][0] = CostFunction(PopPosition[i])
            if PopCost[i][0] < BestCost[0][0]:
                BestCost[0][0] = PopCost[i][0]
                BestSol[0] = PopPosition[i]

        for iter in range(iter_max):

            # Наем пчелы стадии

            # Найти следующий источник меда
            for i in range(nPop):
                while True:
                    k = np.random.randint(0, nPop)
                    if k != i:
                        break
                phi = a*(-1+2*np.random.rand(2))
                NewPosition = PopPosition[i] + phi * \
                    (PopPosition[i]-PopPosition[k])

                # Сделайте жадный выбор
                NewCost = CostFunction(NewPosition)
                if NewCost < PopCost[i][0]:
                    PopPosition[i] = NewPosition
                    PopCost[i][0] = NewCost
                else:
                    Mine[i][0] = Mine[i][0]+1

            # Следуйте за стадией пчелы

            # Рассчитать матрицу вероятности выбора
            Mean = np.mean(PopCost)
            for i in range(nPop):
                Probability[i][0] = np.exp(-PopCost[i][0]/Mean)
            Probability = Probability/np.sum(Probability)
            CumProb = np.cumsum(Probability)

            for k in range(nOnLooker):

                # Выполнить метод выбора рулетки
                m = 0
                for i in range(nPop):
                    m = m + CumProb[i]
                    if m >= np.random.rand(1):
                        break

                # Повторная аренда пчел
                while True:
                    k = np.random.randint(0, nPop)
                    if k != i:
                        break
                phi = a*(-1+2*np.random.rand(2))
                NewPosition = PopPosition[i] + phi * \
                    (PopPosition[i]-PopPosition[k])

                # Сделайте жадный выбор
                NewCost = CostFunction(NewPosition)
                if NewCost < PopCost[i][0]:
                    PopPosition[i] = NewPosition
                    PopCost[i][0] = NewCost
                else:
                    Mine[i][0] = Mine[i][0]+1

            # Обнаружить стадию пчелы
            for i in range(nPop):
                if Mine[i][0] >= L:
                    PopPosition[i] = 8*np.random.rand(1, nVar) - 4
                    PopCost[i][0] = CostFunction(PopPosition[i])
                    Mine[i][0] = 0

            # Сохранить историческое оптимальное решение
            for i in range(nPop):
                if PopCost[i][0] < BestCost[iter+1][0]:
                    BestCost[iter+1][0] = PopCost[i][0]
                    BestSol[iter+1] = PopPosition[i]

        return list(BestSol)

    window_lab_5 = tkinter.Tk()
    window_lab_5.wm_title(
        "Пятая лабораторная. Пчелиный алгоритм оптимизации функции Растригина.")
    window_lab_5.geometry("780x600")
    window_lab_5.resizable(False, False)

    X, Y, Z = get_rastrigin_surface()

    fig = plt.figure()
    fig.add_subplot(projection="3d")

    canvas = FigureCanvasTkAgg(fig, master=window_lab_5)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window_lab_5)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    lbl_1 = Label(window_lab_5, text="Источники")
    lbl_1.pack(side=TOP, padx=5, pady=5)

    txt_1 = Entry(window_lab_5, width=10)
    txt_1.pack(side=TOP, padx=5, pady=5)

    lbl_2 = Label(window_lab_5, text="Кол-во пчёл")
    lbl_2.pack(side=TOP, padx=5, pady=5)

    txt_2 = Entry(window_lab_5, width=10)
    txt_2.pack(side=TOP, padx=5, pady=5)

    lbl_3 = Label(window_lab_5, text="Диапозон")
    lbl_3.pack(side=TOP, padx=5, pady=5)

    txt_3 = Entry(window_lab_5, width=10)
    txt_3.pack(side=TOP, padx=5, pady=5)

    lbl_4 = Label(window_lab_5, text="Iter Max")
    lbl_4.pack(side=TOP, padx=5, pady=5)

    txt_4 = Entry(window_lab_5, width=10)
    txt_4.pack(side=TOP, padx=5, pady=5)

    lbl_5 = Label(window_lab_5, text="Задержка(в сек)")
    lbl_5.pack(side=TOP, padx=5, pady=5)

    txt_5 = Entry(window_lab_5, width=10)
    txt_5.pack(side=TOP, padx=5, pady=5)

    btn = Button(window_lab_5, text="Выполнить", width=20, command=draw)
    btn.pack(side=TOP, padx=5, pady=5, anchor=NW)

    tkinter.mainloop()
