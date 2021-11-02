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

def newton_gradient_descent_plot3D(f, f_vals, X_vals):
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

def newton_convergence_plot(f_vals):
    """plot the convergence process of the algorithm

    :param f_vals: list of the z values along the algorithm process
    :return: None
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(f_vals, color='blue', lw=2)
    ax.set_yscale('log')
    pylab.show()

def newton_backtrack(x0, f, alpha=0.5, beta=0.7):
    """backtrack the guess back such that the result is inside the convex area

    Args:
      x0: the initial values given
      f: given function
      alpha: alpha value between (0, .5)
      beta: beta value between (0, 1)
    Returns:
        t: the step size needed in order to return to the convex area
    """
    t = 1
    return t


def second_order_aprox(f, x0):
    return 0.5 * (nd.Gradient(f)(x0).T @ \
           np.linalg.inv(nd.Hessian(f)(x0)) @ nd.Gradient(f)(x0))

@my_timer
def newton_gradient_descent(x0, f, epsilon, line_search=newton_backtrack, max_iters=1000):
    """ works of convex functions to find the best parameters for the minimum.
        with second order Tylor approximation

    :param x0: initial guess
    :param f: function
    :param epsilon: stopping condition - the magnitude of the target gradient
    :param line_search: method to find the best step size
    :return: [variable value that gives the minimum,
              list of variables along the algorithm process]
    """
    del_x = -np.linalg.inv(nd.Hessian(f)(x0)) @ nd.Gradient(f)(x0)
    t = 1
    points_arr = [x0]
    iters = 1
    while second_order_aprox(f, x0) > epsilon and iters <= max_iters:
        del_x = -np.linalg.inv(nd.Hessian(f)(x0)) @ nd.Gradient(f)(x0)
        t = line_search(x0, f)
        x0 = x0 + t * del_x
        points_arr.append(x0)
        iters += 1
    return x0, points_arr


def newton_f_vals_from_grad_descent(f, cords_list):
    f_vals = []
    for cords in cords_list:
        f_vals.append(f(cords))
    return f_vals




if __name__ == '__main__':
    f = lambda x: x[0]**4 + x[1]**2
    x0 = [1, 1]
    result, time = newton_gradient_descent(x0, f, 1e-10, line_search=newton_backtrack, max_iters=100000)
    X_min, X_vals = result
    f_vals = newton_f_vals_from_grad_descent(f, X_vals)

    print(time)
    newton_convergence_plot(f_vals)
    newton_gradient_descent_plot3D(f, f_vals, X_vals)
