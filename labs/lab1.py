import time
import tkinter
from tkinter import *

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

from .services import funct_consider, make_data


def Lab_1_window():
    def draw():
        print("lAB 1")

        fig.clf()
        
        ax = fig.add_subplot(projection="3d")
        ax.plot_surface(x, y, z, rstride=5, cstride=5,
                        alpha=0.8, cmap="gist_rainbow")
        canvas.draw()

        res_x = txt_1.get()
        res_y = txt_2.get()
        res_step = txt_3.get()
        res_iterations = txt_4.get()

        x_cs, y_cs, z_cs = funct_consider(
            float(res_x), float(res_y), float(res_step), int(res_iterations)
        )

        for i in range(len(x_cs)):
            if i < (len(x_cs) - 1):
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="red", s=1)
            else:
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="black")

            canvas.draw()
            print(
                f"#{i}\tx = {round(x_cs[i], 2)}, y = {round(y_cs[i], 2)}, z = {z_cs[i]}"
            )

            window_lab_1.update()

            delay = 0

            time.sleep(float(delay))
        print("\n")
        
    window_lab_1 = tkinter.Tk()
    window_lab_1.wm_title("Gradient Descent Method")
    window_lab_1.geometry("780x600")
    window_lab_1.resizable(False, False)

    x, y, z = make_data()

    fig = plt.figure()
    fig.add_subplot(projection="3d")

    canvas = FigureCanvasTkAgg(fig, master=window_lab_1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window_lab_1)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    lbl_1 = Label(window_lab_1, text="X")
    lbl_1.pack(side=TOP, padx=5, pady=5)

    txt_1 = Entry(window_lab_1, width=10)
    txt_1.pack(side=TOP, padx=5, pady=5)

    lbl_2 = Label(window_lab_1, text="Y")
    lbl_2.pack(side=TOP, padx=5, pady=5)

    txt_2 = Entry(window_lab_1, width=10)
    txt_2.pack(side=TOP, padx=5, pady=5)

    lbl_3 = Label(window_lab_1, text="Initial step")
    lbl_3.pack(side=TOP, padx=5, pady=5)

    txt_3 = Entry(window_lab_1, width=10)
    txt_3.pack(side=TOP, padx=5, pady=5)

    lbl_4 = Label(window_lab_1, text="Iterations")
    lbl_4.pack(side=TOP, padx=5, pady=5)

    txt_4 = Entry(window_lab_1, width=10)
    txt_4.pack(side=TOP, padx=5, pady=5)

    btn = Button(window_lab_1, text="Выполнить", width=20, command=draw)
    btn.pack(side=TOP, padx=5, pady=5, anchor=NW)

    tkinter.mainloop()
