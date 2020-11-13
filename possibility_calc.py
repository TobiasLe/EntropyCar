from math import factorial
import numpy as np
import matplotlib.pyplot as plt


def number_of_permutations_on_grids(n_objects, grid_spaces):
    n_objects = [n_objects, 0]
    all_possibilities = []
    for x in range(sum(n_objects) + 1):
        n_marbles = [n_objects[0] - x, n_objects[1] + x]
        print(n_marbles)
        possibilities = [None, None]
        for i, (g, n) in enumerate(zip(grid_spaces, n_marbles)):
            possibilities[i] = factorial(g) / factorial(g - n) / factorial(n)
        print(possibilities[0] * possibilities[1])
        all_possibilities.append(possibilities[0] * possibilities[1])
    return all_possibilities


if __name__ == '__main__':
    n_marbles = 9
    grid_spaces = [9, 25]

    number_of_permutations = number_of_permutations_on_grids(n_marbles, grid_spaces)

    fig, axe = plt.subplots()
    axe.plot(number_of_permutations, marker=".", linestyle="")

    fig, axe = plt.subplots()
    axe.plot(np.log(number_of_permutations), marker=".", linestyle="")

    plt.show()
