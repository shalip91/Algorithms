import math
from functools import wraps

import matplotlib.pyplot as plt
import pylab
import numpy as np
import numdifftools as nd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def my_timer(orig_fun):
    import time
    @wraps(orig_fun) #will prevent the stacking problem to occure
    def wrapper(*args, **kwargs):
        start = time.time()
        result = orig_fun(*args, **kwargs)
        time_took = time.time() - start
        # print(f'{orig_fun.__name__} Run in {time_took} sec')
        return result, time_took
    return wrapper


def const_t(x0, f, print_steps=False):
    t = 0.05
    if print_steps: print(f"new t = {t}")
    return t

def gradient_descent_plot3D(f, f_vals, X_vals):
    """ plot a 3D graph of the intire function shape with scatter points
        of the result of gradient descent iterations.

    :param f: function
    :param f_vals: z values
    :param X_vals: x and y values
    :return: None
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = y = np.arange(-1, 1.0, 0.05)
    X, Y = np.meshgrid(x, y)
    zs = np.array([f([x, y]) for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)
    ax.plot_surface(X, Y, Z, alpha=0.2)
    ax.scatter(xs=np.array(X_vals)[:, 0], ys=np.array(X_vals)[:, 1], zs=f_vals, color='red', lw=5)
    plt.show()

def convergence_plot(f_vals):
    """plot the convergence process of the algorithm

    :param f_vals: list of the z values along the algorithm process
    :return: None
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(f_vals, color='blue', lw=2)
    ax.set_yscale('log')
    pylab.show()

def print_backtrack_steps(f, x0, t, del_x, alpha):
    print(f"f(x0 + t*" + u"\u0394" + "x" + f") = f({np.round(x0, 4)} + {t}*{np.round(del_x, 4)}) = {np.round(f(x0 + t * del_x),4)} > "
          f"f(x0) + " + u"\u03B1" + " * t * " + u"\u2207" + "f"  + u"\u0394" + "x" + " = "
          f"{np.round(f(x0), 4)} + {alpha} * {t} * {np.round(np.dot(nd.Gradient(f)(x0), del_x), 4)} = "
          f"{np.round(f(x0) + alpha * t * np.dot(nd.Gradient(f)(x0), del_x), 4)}")


def GD_backtrack(x0, f, alpha=0.5, beta=0.7,print_steps=True):
    """backtrack the guess back such that the result is inside the convex area

    Args:
      x0: the initial values given
      f: given function
      alpha: alpha value between (0, .5)
      beta: beta value between (0, 1)
    Returns:
        t: the step size needed in order to return to the convex area
    """
    t=0.08
    del_x = -nd.Gradient(f)(x0)
    while f(x0 + t*del_x) > f(x0) + alpha * t * np.dot(nd.Gradient(f)(x0), del_x):
        if print_steps: print_backtrack_steps(f, x0, t, del_x, alpha)
        t *= beta
        if print_steps: print(f"new t = {t}")
    if print_steps: print_backtrack_steps(f, x0, t, del_x, alpha)

    return t

@my_timer
def gradient_descent(x0, f, epsilon, line_search=GD_backtrack, max_iters=1000, print_steps=True):
    """ works of convex functions to find the best parameters for the minimum.

    :param x0: initial guess
    :param f: function
    :param epsilon: stopping condition - the magnitude of the target gradient
    :param line_search: method to find the best step size
    :return: [variable value that gives the minimum,
              list of variables along the algorithm process]
    """
    del_x = -nd.Gradient(f)(x0)
    t = 1
    points_arr = [x0]
    iters = 1
    while math.sqrt(np.dot(del_x, del_x)) > epsilon and iters <= max_iters:
        del_x = np.round(-nd.Gradient(f)(x0),4)
        if print_steps:
            print(f'\niter number: {iters}')
            print(u"\u0394" + "x" + f" = -" + u"\u2207" + f'f(x0) = {del_x}')
        t = line_search(x0, f, print_steps=print_steps)
        x0 = x0 + t * del_x
        if print_steps:
            print(f'x0 = x0 + t * ' + u"\u0394" + "x" + f' = {np.round(x0,4)}')
        points_arr.append(x0)
        iters += 1
    return x0, points_arr


def GD_f_vals_from_grad_descent(f, cords_list):
    f_vals = []
    for cords in cords_list:
        f_vals.append(f(cords))
    return f_vals




if __name__ == '__main__':
    f = lambda x: x[0]**20 + x[1]**2
    x0 = [1, 1]
    result, time = gradient_descent(x0, f, 1e-3, line_search=GD_backtrack, max_iters=100000, print_steps=False)
    X_min, X_vals = result
    f_vals = GD_f_vals_from_grad_descent(f, X_vals)

    print(time)
    convergence_plot(f_vals)
    gradient_descent_plot3D(f, f_vals, X_vals)
