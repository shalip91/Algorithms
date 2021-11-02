from gradient_descent import *
from newton import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    f = lambda x: x[0]**4 + x[1]**2
    x0 = [1, 1]

    epsilons = np.linspace(1e-3, 1e-4,5)
    GD_times = []
    N_times = []
    for e in epsilons:
        print("hhhhhhhhhhhhhhhhhhhhhhh")
        _, time_GD = gradient_descent(x0, f, e, line_search=GD_backtrack, max_iters=100000, print_steps=False)
        _, time_N = newton_gradient_descent(x0, f, e, line_search=newton_backtrack, max_iters=100000)
        GD_times.append(time_GD)
        N_times.append(time_N)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(GD_times)
    ax.plot(N_times)
    plt.show()
