import copy
from itertools import combinations

import numpy as np
import pylab
from mpl_toolkits.mplot3d import Axes3D

import tkinter
from tkinter import *
from tkinter import scrolledtext

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import numpy as np
import time


def Lab_3_window():
    def rosenbrock(x, y):
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

    class GeneticEvolution:
        def __init__(self, func, mut_prob=0.8, kill_portion=0.2, max_pairs=1000):
            self.func = func
            self.population = []
            self.mutation_probability = mut_prob
            self.portion = kill_portion
            self.max_pairs = max_pairs
            self.old_point = []


        def generate_random_population(self, min, max, size=200):
            self.population = np.random.random_integers(min, max, (size, 2)).tolist()
            self.old_point = self.population

        def initialize(self, min, max):
            self.generate_random_population(min, max)

        def killing(self, population):
            res = np.argsort([self.func(item[0], item[1]) for item in population])
            res = res[:np.random.poisson(int(len(population) * self.portion))]
            return np.array(population)[res].tolist()

        def crossover(self, a, b, prob=0.5):
            return [a[0], b[1]] if np.random.rand() > prob else [b[0], a[1]]

        def mutate(self, a):
            if np.random.rand() < self.mutation_probability:
                new_a = a + (np.random.rand(1) - 0.5) * 0.05
            else:
                new_a = a
            return new_a

        def evolute(self, n_steps=100):
            for n in range(n_steps):
                ind = 0
                new_population = copy.copy(self.population)
                for comb in combinations(range(len(self.population)), 2):
                    ind += 1
                    if ind > self.max_pairs:
                        break
                    a = self.mutate(self.population[comb[0]])
                    b = self.mutate(self.population[comb[1]])
                    new_item = self.crossover(a, b)
                    new_population.append(new_item)
                self.old_point += new_population
                self.population = self.killing(new_population)


            return self.old_point + self.population

    def get_rosenbrock_surface():
        x = np.arange(-2.0, 2.0, 0.01)
        y = np.arange(-1.0, 3.0, 0.01)
        x_grid, y_grid = np.meshgrid(x, y)

        z_grid = rosenbrock(x_grid, y_grid)
        return x_grid, y_grid, z_grid


    def draw():
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(X, Y, Z, rstride=10, cstride=10, alpha=0.4, cmap="seismic")
        canvas.draw()
        min = txt_1.get()
        max = txt_2.get()
        g = GeneticEvolution(func=rosenbrock)
        g.initialize(min, max)
        point = g.evolute()
        for pn in point:
            func = rosenbrock(pn[0], pn[1])
            if func != 0.0:
                ax.scatter(pn[0], pn[1], func, c="black", s=3)
                print(f"Значение функции = {func} в точке x = {pn[0]}, y = {pn[1]}\n")

            else:
                ax.scatter(pn[0], pn[1], func, c="red", s=3)
                print(f'Наименьшее значение функции = {func} в точке x={pn[0]}, y={pn[1]}')

                break

            canvas.draw()
            window_lab_3.update()
            delay = txt_5.get()
            time.sleep(float(delay))

    window_lab_3 = tkinter.Tk()
    window_lab_3.wm_title("Третья лабораторная. Генетический алгоритм оптимизации функции Розенброкка.")
    window_lab_3.geometry("780x600")
    window_lab_3.resizable(False, False)

    X, Y, Z = get_rosenbrock_surface()

    fig = plt.figure()
    fig.add_subplot(projection="3d")

    canvas = FigureCanvasTkAgg(fig, master=window_lab_3)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window_lab_3)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    lbl_1 = Label(window_lab_3, text="Min")
    lbl_1.pack(side=TOP, padx=5, pady=5)

    txt_1 = Entry(window_lab_3, width=10)
    txt_1.pack(side=TOP, padx=5, pady=5)

    lbl_2 = Label(window_lab_3, text="Max")
    lbl_2.pack(side=TOP, padx=5, pady=5)

    txt_2 = Entry(window_lab_3, width=10)
    txt_2.pack(side=TOP, padx=5, pady=5)

    lbl_3 = Label(window_lab_3, text="Задержка(в сек)")
    lbl_3.pack(side=TOP, padx=5, pady=5)

    txt_5 = Entry(window_lab_3, width=10)
    txt_5.pack(side=TOP, padx=5, pady=5)

    btn = Button(window_lab_3, text="Выполнить", width=20, command=draw)
    btn.pack(side=TOP, padx=5, pady=5, anchor=NW)

    tkinter.mainloop()
