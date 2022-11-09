import time
import tkinter
from tkinter import *
from tkinter import scrolledtext

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def Lab_2_window():
    def f(xgrid, ygrid):
        return (
            2 * np.power(xgrid, 2)
            + 3 * np.power(ygrid, 2)
            + (4 * xgrid * ygrid)
            - (6 * xgrid)
            - (3 * ygrid)
        )

    def get_index(func, elem):
        for i in range(len(func)):
            if func[i] == elem:
                return i
        return 0

    def simplex_method(x1, x2):
        triangle = []
        x0 = float(x1)
        z0 = float(x2)
        e = 5
        alpha = 2
        points = [
            [x0 - alpha / 2, z0 - 0.29 * alpha],
            [x0 + alpha / 2, z0 - 0.29 * alpha],
            [x0, z0 + 0.58 * alpha],
        ]
        func = [
            f(points[0][0], points[0][1]),
            f(points[1][0], points[1][1]),
            f(points[2][0], points[2][1]),
        ]
        triangle.append(list(points))
        x_min = x0
        z_min = z0
        y_min = f(x0, z0)
        flag = 0
        x_max = x0
        z_max = z0
        while abs(f(x_max, z_max) - min(func)) > e:
            if flag:
                flag = 0
                x0, z0 = points[get_index(func, min(func))]
                x0 += points[get_index(func, max(func))][0]
                z0 += points[get_index(func, max(func))][1]
                x0 /= 2
                z0 /= 2
                points.remove(points[get_index(func, max(func))])
                func.remove(max(func))
                x1, z1 = points[get_index(func, min(func))]
                x1 += points[get_index(func, max(func))][0]
                z1 += points[get_index(func, max(func))][1]
                x1 /= 2
                z1 /= 2
                points.remove(points[get_index(func, max(func))])
                func.remove(max(func))
                func.append(f(x0, z0))
                points.append([x0, z0])
                func.append(f(x1, z1))
                points.append([x1, z1])
            else:
                x_max, z_max = points[get_index(func, max(func))]
                points.remove(points[get_index(func, max(func))])
                func.remove(max(func))
                x0 = 0 - x_max
                z0 = 0 - z_max
                for value in points:
                    x0 += value[0]
                    z0 += value[1]
                if f(x0, z0) > max(func):
                    func.append(f(x_max, z_max))
                    points.append([x_max, z_max])
                    flag = 1
                else:
                    func.append(f(x0, z0))
                    points.append([x0, z0])

            if f(x_min, z_min) > min(func):
                x_min, z_min = points[get_index(func, min(func))]
                y_min = min(func)

            triangle.append(list(points))

        x_min = round(x_min, 2)
        z_min = round(z_min, 2)
        y_min = round(y_min, 2)
        return triangle, x_min, y_min, z_min

    def draw():
        fig.clf()
        ax = fig.add_subplot(projection="3d")
        ax.plot_surface(x, y, z, rstride=10, cstride=10,
                        alpha=0.4, cmap="seismic")
        canvas.draw()
        x1 = txt_1.get()
        x2 = txt_2.get()
        triangle, X, Z, Y = simplex_method(x1, x2)
        for tr in triangle:
            if min(tr)[1] > Y:
                ax.scatter(tr[0][0], tr[0][1], min(tr), c="black", s=3)
                print(
                    f"x = {round(tr[0][0], 2)} , y = {round(tr[0][1], 2)} , z = {min(tr)[1]}\n"
                )
            else:
                ax.scatter(X, Y, Z, c="red", s=3)
                print(f"x = {round(X, 2)} , y = {Y}, z = {Z}\n")
            canvas.draw()
            window_lab_2.update()
            delay = txt_5.get()
            time.sleep(float(delay))

    def makeData():
        # Строим сетку в интервале от -10 до 10, имеющую 100 отсчетов по обоим координатам
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)

        # Создаем двумерную матрицу-сетку
        xgrid, ygrid = np.meshgrid(x, y)

        z = f(xgrid, ygrid)
        return xgrid, ygrid, z

    window_lab_2 = tkinter.Tk()
    window_lab_2.wm_title(
        "Вторая лабораторная. Квадратичное программирование.")
    window_lab_2.geometry("780x600")

    x, y, z = makeData()

    fig = plt.figure()
    fig.add_subplot(projection="3d")

    canvas = FigureCanvasTkAgg(fig, master=window_lab_2)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window_lab_2)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    lbl_1 = Label(window_lab_2, text="X1")
    lbl_1.pack(side=TOP, padx=5, pady=5)

    txt_1 = Entry(window_lab_2, width=10)
    txt_1.pack(side=TOP, padx=5, pady=5)

    lbl_2 = Label(window_lab_2, text="X2")
    lbl_2.pack(side=TOP, padx=5, pady=5)

    txt_2 = Entry(window_lab_2, width=10)
    txt_2.pack(side=TOP, padx=5, pady=5)

    lbl_6 = Label(window_lab_2, text="Задержка(в сек)")
    lbl_6.pack(side=TOP, padx=5, pady=5)

    txt_5 = Entry(window_lab_2, width=10)
    txt_5.pack(side=TOP, padx=5, pady=5)

    btn = Button(window_lab_2, text="Выполнить", width=20, command=draw)
    btn.pack(side=TOP, padx=5, pady=5, anchor=NW)

    tkinter.mainloop()
