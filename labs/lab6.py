import random
import time
import tkinter
from operator import itemgetter
from tkinter import *

import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def Lab_6_window():
    def CostFunction(x, y):
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

    def get_rosenbrock_surface():
        x = np.arange(-2.0, 2.0, 0.01)
        y = np.arange(-1.0, 3.0, 0.01)
        x_grid, y_grid = np.meshgrid(x, y)

        z_grid = CostFunction(x_grid, y_grid)
        return x_grid, y_grid, z_grid

    class Immunity:
        def __init__(self, func, agents, clons, best, best_clon_numb, position_x, position_y):
            self.func = func

            self.pos_x = float(position_x)
            self.pos_y = float(position_y)

            self.agents_numb = agents
            self.agents = [[random.uniform(-self.pos_x, self.pos_x), random.uniform(-self.pos_y, self.pos_y), 0.0] for _ in
                           range(self.agents_numb)]

            for i in self.agents:
                i[2] = self.func(i[0], i[1])

            self.best = best
            self.best_clon_numb = best_clon_numb
            self.clon_numb = clons

        def immune_step(self, coef):

            best_pop = sorted(self.agents, key=itemgetter(2),
                              reverse=False)[:self.best]

            new_pop = list()
            for pop in best_pop:
                for _ in range(self.clon_numb):
                    new_pop.append(pop.copy())

            for npop in new_pop:
                npop[0] = npop[0] + coef * random.uniform(-0.5, 0.5)
                npop[1] = npop[1] + coef * random.uniform(-0.5, 0.5)
                npop[2] = self.func(npop[0], npop[1])

            new_pop = sorted(new_pop, key=itemgetter(2), reverse=False)[
                :self.best_clon_numb]

            self.agents += new_pop
            self.agents = sorted(self.agents, key=itemgetter(
                2), reverse=False)[:self.agents_numb]

        def get_best(self):
            return self.agents[0]

    def draw():
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(X, Y, Z, rstride=10, cstride=10,
                        alpha=0.4, cmap="seismic")
        canvas.draw()
        pop_number = int(txt_1.get())
        clon = int(txt_2.get())
        best_pop = int(txt_3.get())
        best_clon = int(txt_4.get())
        myImmune = Immunity(CostFunction, pop_number, clon,
                            best_pop, best_clon, 5, 5)
        # func - используемая функция
        # pop_number - размер популяции
        # clon - кол-во клонов
        # best_pop - сколько выбираем лучших из популяции
        # best_clon - сколько выбираем лучших из клонов
        # pos_x, pos_y - границы графика
        maxIter = 60
        for i in range(maxIter):
            myImmune.immune_step(1/(i+1))
            pn = myImmune.get_best()
            if i != maxIter - 1:
                ax.scatter(pn[0], pn[1], pn[2], c="black", s=3)
                print(
                    f"№{i}. Значение функции = {pn[2]} в точке x = {pn[0]}, y = {pn[1]}")
            else:
                ax.scatter(pn[0], pn[1], pn[2], c="red", s=10)
                print(
                    f'Наименьшее значение функции = {pn[2]} в точке x={pn[0]}, y={pn[1]}')
                break
            canvas.draw()
            window_lab_6.update()
            delay = txt_5.get()
            time.sleep(float(delay))

    window_lab_6 = tkinter.Tk()
    window_lab_6.wm_title(
        "Шестая лабораторная. Алгоритм искусственной иммунной сети оптимизации функции Розенброка.")
    window_lab_6.geometry("800x600")
    window_lab_6.resizable(False, False)

    X, Y, Z = get_rosenbrock_surface()

    fig = plt.figure()
    fig.add_subplot(projection="3d")

    canvas = FigureCanvasTkAgg(fig, master=window_lab_6)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window_lab_6)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    lbl_1 = Label(window_lab_6, text="Размер популяции")
    lbl_1.pack(side=TOP, padx=5, pady=5)

    txt_1 = Entry(window_lab_6, width=10)
    txt_1.pack(side=TOP, padx=5, pady=5)

    lbl_2 = Label(window_lab_6, text="Кол-во клонов")
    lbl_2.pack(side=TOP, padx=5, pady=5)

    txt_2 = Entry(window_lab_6, width=10)
    txt_2.pack(side=TOP, padx=5, pady=5)

    lbl_3 = Label(window_lab_6, text="Лучшие из популяции")
    lbl_3.pack(side=TOP, padx=5, pady=5)

    txt_3 = Entry(window_lab_6, width=10)
    txt_3.pack(side=TOP, padx=5, pady=5)

    lbl_4 = Label(window_lab_6, text="Лучшие из клонов")
    lbl_4.pack(side=TOP, padx=5, pady=5)

    txt_4 = Entry(window_lab_6, width=10)
    txt_4.pack(side=TOP, padx=5, pady=5)

    lbl_5 = Label(window_lab_6, text="Задержка(в сек)")
    lbl_5.pack(side=TOP, padx=5, pady=5)

    txt_5 = Entry(window_lab_6, width=10)
    txt_5.pack(side=TOP, padx=5, pady=5)

    btn = Button(window_lab_6, text="Выполнить", width=20, command=draw)
    btn.pack(side=TOP, padx=5, pady=5, anchor=NW)

    tkinter.mainloop()
