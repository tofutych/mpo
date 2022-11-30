import time
import tkinter
from random import random
from tkinter import *
from typing import List
import matplotlib.animation
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
# Хемотаксис - это двигательная реация микроогранизмов на химический раздражитель. 
# Репродукция - цель механизм - ускорение сходимости алгоритма(интенсификация)
#         Текущее здоровье - сумма значений фитнес-функции во всех точках траектории бактерии.

# Ликвидация и рассеивание. Хемотаксиса и репродукции обычно недостаточно, потому что эти процедуры
# не позволяют бактериям покидать райденные ими локальные минимумы(максимумы). Поэтому вводятся ликвидация 
# и рассеивание. которые призваны преодолеть этот недостаток.
#     Механизм ликвидации и рассеивания включается после выполнения некоторого числа процедур репродукции
#      и состоит в следующем: С заданной вероятностью выбираем n < S бактерий и уничтожаем их))))
#      Вместо уничтоженных в случайной точке пространства создаем нового агента с тем же номером. Число
#      бактерий после геноцида должно быть таким же как и в начале.

def Lab_7_window():
    def cost_function(input):
        x = input[0]
        y = input[1]
        result = -((x ** 2) + (y ** 2))
        return result

    def get_rastrigin_surface():
        X = np.linspace(-5, 5, 200)
        Y = np.linspace(-5, 5, 200)
        X, Y = np.meshgrid(X, Y)
        Z = cost_function([X, Y])
        return X, Y, Z

    class SW(object):
        def __init__(self):
            self.__Positions = []
            self.__Gbest = []

        def _set_Gbest(self, Gbest):
            self.__Gbest = Gbest

        def _points(self, agents):
            self.__Positions.append([list(i) for i in agents])

        def get_agents(self):
            """Returns a history of all agents of the algorithm (return type:
            list)"""

            return self.__Positions

        def get_Gbest(self):
            """Return the best position of algorithm (return type: list)"""

            return list(self.__Gbest)

    class bfo(SW):
        def __init__(self, n, function, dimension, iteration, lb=-5, ub=5,
                     Nc=2, Ns=12, C=0.2, Ped=1.15):
            """
            n - колво агентов
            Nc - количество хемотаксических шагов (default value is 2)
            Ns - максимальное число шагов вдоль выбранного направления (default value is 12)
            C - размер шага (default value is 0.2)
            Ped - вероятность уничтожения бактерии (default value is 1.15)
            """
            super(bfo, self).__init__()

            self.__agents = np.random.uniform(lb, ub, (n, dimension))

            self._points(self.__agents)

            n_is_even = True
            if n & 1:
                n_is_even = False

            J = np.array([function(x) for x in self.__agents])
            Pbest = self.__agents[J.argmin()]
            Gbest = Pbest

            C_list = [C - C * 0.9 * i / iteration for i in range(iteration)]
            Ped_list = [Ped - Ped * 0.5 * i /
                        iteration for i in range(iteration)]

            J_last = J[::1]

            # начало хемотаксиса
            for t in range(iteration):
                J_chem = [J[::1]]

                for j in range(Nc):
                    for i in range(n):
                        dell = np.random.uniform(-1, 1, dimension)
                        self.__agents[i] += C_list[t] * \
                            np.linalg.norm(dell) * dell

                        for m in range(Ns):
                            if function(self.__agents[i]) > J_last[i]:
                                J_last[i] = J[i]
                                self.__agents[i] += C_list[t] * np.linalg.norm(dell) \
                                    * dell
                            else:
                                dell = np.random.uniform(-1, 1, dimension)
                                self.__agents[i] += C_list[t] * np.linalg.norm(dell) \
                                    * dell

                    J = np.array([function(x) for x in self.__agents])
                    J_chem += [J]

                J_chem = np.array(J_chem)

                # выбрали живчиков
                J_health = [(sum(J_chem[:, i]), i) for i in range(n)]
                J_health.sort(reverse=True)
                alived_agents = []
                for i in J_health:
                    alived_agents += [list(self.__agents[i[1]])]

                # репродукция и рассеивания
                if n_is_even:
                    alived_agents = 2 * alived_agents[:n // 2]
                    self.__agents = np.array(alived_agents)
                else:
                    alived_agents = 2 * alived_agents[:n // 2] + \
                        [alived_agents[n // 2]]
                    self.__agents = np.array(alived_agents)

                if t < iteration - 2:
                    for i in range(n):
                        r = random()
                        if r <= Ped_list[t]:
                            self.__agents[i] = np.random.uniform(
                                lb, ub, dimension)

                J = np.array([function(x) for x in self.__agents])
                self._points(self.__agents)

                Pbest = self.__agents[J.argmin()]
                if function(Pbest) > function(Gbest):
                    Gbest = Pbest

            self._set_Gbest(Gbest)
            print(Gbest)

    def draw():
        agents = int(txt_1.get())
        dimenssion = int(txt_2.get())
        iteration = int(txt_3.get())
        bf = bfo(agents, cost_function, dimenssion, iteration)
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(X, Y, Z, rstride=10, cstride=10,
                        alpha=0.4, cmap="seismic")
        canvas.draw()
        agents = bf.get_agents()
        iter = len(agents)
        n = len(agents[0])
        t = np.array([np.ones(n) * i for i in range(iter)]).flatten()
        b = []
        [[b.append(agent) for agent in epoch] for epoch in agents]
        c = [cost_function(x) for x in b]
        a = np.asarray(b)
        # print(f'x: {a[:, 0]},  y: {a[:, 1]}, z: {c}\n')
        df = pd.DataFrame({"time": t, "x": a[:, 0], "y": a[:, 1], "z": c})

        def update_graph(num):
            if num != iter - 1:
                graph.set_facecolor('black')
                data = df[df['time'] == num]
                graph._offsets3d = (data.x, data.y, data.z)
                title.set_text(cost_function.__name__ + " " * 45 + 'iteration: {}'.format(
                    num))
                delay = txt_5.get()
                time.sleep(float(delay))
                canvas.draw()
                window_lab_7.update()
            else:
                data = df[df['time'] == num]
                title.set_text("FINAL")
                graph.set_facecolor('red')
                graph._offsets3d = (data.x, data.y, data.z)
                canvas.draw()
                window_lab_7.update()
                return

        title = ax.set_title(cost_function.__name__ +
                             " " * 45 + f'iteration: {0}')
        data = df[df['time'] == 0]
        graph = ax.scatter(data.x, data.y, data.z, color='black')

        ani = matplotlib.animation.FuncAnimation(fig, update_graph, iter,
                                                 interval=.001, blit=False, repeat=False)
        # ani.save('result.gif')
        canvas.draw()
        window_lab_7.update()

    window_lab_7 = tkinter.Tk()
    window_lab_7.wm_title(
        "Седьмая лабораторная. Алгоритм бактериальной оптимизации обратной сферической функции.")
    window_lab_7.geometry("780x600")
    window_lab_7.resizable(False, False)

    X, Y, Z = get_rastrigin_surface()

    fig = plt.figure()
    fig.add_subplot(projection="3d")

    canvas = FigureCanvasTkAgg(fig, master=window_lab_7)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window_lab_7)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    lbl_1 = Label(window_lab_7, text="Агенты")
    lbl_1.pack(side=TOP, padx=5, pady=5)

    txt_1 = Entry(window_lab_7, width=10)
    txt_1.pack(side=TOP, padx=5, pady=5)

    lbl_2 = Label(window_lab_7, text="Измерение")
    lbl_2.pack(side=TOP, padx=5, pady=5)

    txt_2 = Entry(window_lab_7, width=10)
    txt_2.pack(side=TOP, padx=5, pady=5)

    lbl_3 = Label(window_lab_7, text="Итерации")
    lbl_3.pack(side=TOP, padx=5, pady=5)

    txt_3 = Entry(window_lab_7, width=10)
    txt_3.pack(side=TOP, padx=5, pady=5)

    lbl_5 = Label(window_lab_7, text="Задержка(в сек)")
    lbl_5.pack(side=TOP, padx=5, pady=5)

    txt_5 = Entry(window_lab_7, width=10)
    txt_5.pack(side=TOP, padx=5, pady=5)

    btn = Button(window_lab_7, text="Выполнить", width=20, command=draw)
    btn.pack(side=TOP, padx=5, pady=5, anchor=NW)

    tkinter.mainloop()
