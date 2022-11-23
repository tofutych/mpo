import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# Функция Растригина
def f(x, y):
    return (x**2 - 10 * np.cos(2 * np.pi * x)) + \
            (y**2 - 10 * np.cos(2 * np.pi * y)) + 20

# Global Minima
x, y = np.array(np.meshgrid(np.linspace(0, 5, 100), np.linspace(0, 5, 100)))
z = f(x, y)
x_min = x.ravel()[z.argmin()]
y_min = y.ravel()[z.argmin()]
print("Global Minima : f({}) = {}".format([x_min, y_min], f(x_min, y_min)))

# PSO Parameters
c1 = c2 = 0.1
w = 0.8

# Population Init
population_size = 20
np.random.seed(100)
X = np.random.rand(2, population_size) * 5
V = np.random.randn(2, population_size) * 0.1
pbest = X
pbest_obj = f(X[0], X[1])
gbest = pbest[:, pbest_obj.argmin()]
gbest_obj = pbest_obj.min()


def update():
    global V, X, pbest, pbest_obj, gbest, gbest_obj
    # PSO Parameters
    r1, r2 = np.random.rand(2)
    V = w * V + c1 * r1 * (pbest - X) + c2 * r2 * (gbest.reshape(-1, 1) - X)
    X = X + V
    obj = f(X[0], X[1])
    pbest[:, (pbest_obj >= obj)] = X[:, (pbest_obj >= obj)]
    pbest_obj = np.array([pbest_obj, obj]).min(axis=0)
    gbest = pbest[:, pbest_obj.argmin()]
    gbest_obj = pbest_obj.min()



for i in range(1, 50):
    # prev = gbest_obj
    update()
    print("PSO {} : f({}) = {}".format(i, gbest, gbest_obj))
