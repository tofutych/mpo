import time
import tkinter
from tkinter import *

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def Lab_4_window():
    def rastrigin(x, y):
        return (x ** 2 - 10 * np.cos(2 * np.pi * x)) + \
               (y ** 2 - 10 * np.cos(2 * np.pi * y)) + 20

    def get_rastrigin_surface():
        X = np.linspace(-4, 4, 200)
        Y = np.linspace(-4, 4, 200)

        X, Y = np.meshgrid(X, Y)

        Z = rastrigin(X, Y)
        return X, Y, Z

    def update(C1, C2, W, Size):
        # PSO Parameters
        c1 = C1
        c2 = C2
        w = W
        # Population Init
        population_size = Size
        np.random.seed(100)
        X = np.random.rand(2, population_size) * 5
        V = np.random.randn(2, population_size) * 0.1
        pbest = X
        pbest_obj = rastrigin(X[0], X[1])
        gbest = pbest[:, pbest_obj.argmin()]
        gbest_obj = pbest_obj.min()
        point = []
        # PSO Parameters
        for i in range(50):
            r1, r2 = np.random.rand(2)
            # скорость частиц
            V = w * V + c1 * r1 * (pbest - X) + c2 * \
                r2 * (gbest.reshape(-1, 1) - X)
            # корректируем текущую координату каждой частицы
            X = X + V
            obj = rastrigin(X[0], X[1])
            pbest[:, (pbest_obj >= obj)] = X[:, (pbest_obj >= obj)]
            pbest_obj = np.array([pbest_obj, obj]).min(axis=0)
            gbest = pbest[:, pbest_obj.argmin()]
            gbest_obj = pbest_obj.min()
            point.append([gbest[0], gbest[1], gbest_obj])
        return point

    def draw():
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(X, Y, Z, rstride=10, cstride=10,
                        alpha=0.4, cmap="seismic")
        canvas.draw()
        C1 = txt_1.get()
        C2 = txt_2.get()
        W = txt_3.get()
        size = txt_4.get()
        point = update(float(C1), float(C2), float(W), int(size))
        for pn in point:
            if point[::-1].index(pn) != 0:
                ax.scatter(pn[0], pn[1], pn[2], c="black", s=3)
                print(
                    f"Значение функции = {pn[2]} в точке x = {pn[0]}, y = {pn[1]}\n")
            else:
                ax.scatter(pn[0], pn[1], pn[2], c="red", s=10)
                print(
                    f'Наименьшее значение функции = {pn[2]} в точке x={pn[0]}, y={pn[1]}')
                break
            canvas.draw()
            window_lab_4.update()
            delay = txt_5.get()
            time.sleep(float(delay))

    window_lab_4 = tkinter.Tk()
    window_lab_4.wm_title(
        "Четвёртая лабораторная. Алгоритм роя частиц оптимизации функции Растригина.")
    window_lab_4.geometry("780x600")
    window_lab_4.resizable(False, False)

    X, Y, Z = get_rastrigin_surface()

    fig = plt.figure()
    fig.add_subplot(projection="3d")

    canvas = FigureCanvasTkAgg(fig, master=window_lab_4)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window_lab_4)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    lbl_1 = Label(window_lab_4, text="С1")
    lbl_1.pack(side=TOP, padx=5, pady=5)

    txt_1 = Entry(window_lab_4, width=10)
    txt_1.pack(side=TOP, padx=5, pady=5)

    lbl_2 = Label(window_lab_4, text="С2")
    lbl_2.pack(side=TOP, padx=5, pady=5)

    txt_2 = Entry(window_lab_4, width=10)
    txt_2.pack(side=TOP, padx=5, pady=5)

    lbl_3 = Label(window_lab_4, text="W")
    lbl_3.pack(side=TOP, padx=5, pady=5)

    txt_3 = Entry(window_lab_4, width=10)
    txt_3.pack(side=TOP, padx=5, pady=5)

    lbl_4 = Label(window_lab_4, text="Размер популяции")
    lbl_4.pack(side=TOP, padx=5, pady=5)

    txt_4 = Entry(window_lab_4, width=10)
    txt_4.pack(side=TOP, padx=5, pady=5)

    lbl_5 = Label(window_lab_4, text="Задержка(в сек)")
    lbl_5.pack(side=TOP, padx=5, pady=5)

    txt_5 = Entry(window_lab_4, width=10)
    txt_5.pack(side=TOP, padx=5, pady=5)

    btn = Button(window_lab_4, text="Выполнить", width=20, command=draw)
    btn.pack(side=TOP, padx=5, pady=5, anchor=NW)

    tkinter.mainloop()
