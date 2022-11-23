import numpy as np
import pylab
from mpl_toolkits.mplot3d import Axes3D
import pyswarms as ps
from pyswarms.utils.plotters.plotters import plot_cost_history
from matplotlib import animation


def rosenbrock(args):
    x, y = args[0], args[1]
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


def rosenbrock_fun(x):
    x = np.array(x)
    result = np.sum((1 - x.T[:-1]) ** 2.0 + 100 * (x.T[1:] - x.T[:-1] ** 2.0) ** 2, axis=0)
    return result
import numpy as np
import pylab
from mpl_toolkits.mplot3d import Axes3D
import pyswarms as ps
from pyswarms.utils.plotters.plotters import plot_cost_history
from matplotlib import animation


def rosenbrock(args):
    x, y = args[0], args[1]
    return (x ** 2 - 10 * np.cos(2 * np.pi * x)) + \
               (y ** 2 - 10 * np.cos(2 * np.pi * y)) + 20


def rosenbrock_fun(x):
    x = np.array(x)
    result = np.sum(x.T[:-1] ** 2 - 10 * np.cos(2 * np.pi * x.T[:-1]), axis=0)
    return result


def get_rosenbrock_surface():
    x = np.arange(-2, 2, 0.1)
    y = np.arange(-2, 2, 0.1)
    xgrid, ygrid = np.meshgrid(x, y)
    zgrid = rosenbrock([xgrid, ygrid])
    return xgrid, ygrid, zgrid


def animate(i, coords):
    x = coords[i][:, 0]
    y = coords[i][:, 1]
    z = np.array([rosenbrock(elem) for elem in coords[i]])

    dots.set_data(x, y)
    dots.set_3d_properties(z)


options = {'c1': 0.3, 'c2': 0.2, 'w': 0.9}
optimizer = ps.single.GlobalBestPSO(n_particles=20, dimensions=2, options=options)
optimizer.optimize(rosenbrock_fun, iters=100)

plot_cost_history(optimizer.cost_history)

x, y, z = get_rosenbrock_surface()
fig = pylab.figure()
axes = Axes3D(fig)
axes.plot_surface(x, y, z, alpha=0.2)
pos_h = optimizer.pos_history

dots, = axes.plot(pos_h[0][:, 0], pos_h[0][:, 1], [rosenbrock(elem) for elem in pos_h[0]],
                  marker='o', c='red', linestyle='')

anim = animation.FuncAnimation(fig, animate, fargs=(pos_h,), interval=200, repeat=True)
anim.save('result.gif', writer='imagemagick', dpi=96)


def get_rosenbrock_surface():
    x = np.arange(-2, 2, 0.1)
    y = np.arange(-2, 2, 0.1)
    xgrid, ygrid = np.meshgrid(x, y)
    zgrid = rosenbrock([xgrid, ygrid])
    return xgrid, ygrid, zgrid


def animate(i, coords):
    x = coords[i][:, 0]
    y = coords[i][:, 1]
    z = np.array([rosenbrock(elem) for elem in coords[i]])
    print(z)
    dots.set_data(x, y)
    dots.set_3d_properties(z)


options = {'c1': 0.3, 'c2': 0.2, 'w': 0.9}
optimizer = ps.single.GlobalBestPSO(n_particles=20, dimensions=2, options=options)
optimizer.optimize(rosenbrock_fun, iters=100)

plot_cost_history(optimizer.cost_history)

x, y, z = get_rosenbrock_surface()
fig = pylab.figure()
axes = Axes3D(fig)
axes.plot_surface(x, y, z, alpha=0.2)
pos_h = optimizer.pos_history

dots, = axes.plot(pos_h[0][:, 0], pos_h[0][:, 1], [rosenbrock(elem) for elem in pos_h[0]],
                  marker='o', c='red', linestyle='')

anim = animation.FuncAnimation(fig, animate, fargs=(pos_h,), interval=200, repeat=True)
anim.save('result.gif', writer='imagemagick', dpi=96)