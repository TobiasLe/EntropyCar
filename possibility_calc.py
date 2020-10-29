from math import factorial
import numpy as np
import matplotlib.pyplot as plt

n_marbles_start = [9, 0]
grid_spaces = [9, 25]

all_possibilities = []
for x in range(sum(n_marbles_start) + 1):
    n_marbles = [n_marbles_start[0] - x, n_marbles_start[1] + x]
    print(n_marbles)
    possibilities = [None, None]
    for i, (g, n) in enumerate(zip(grid_spaces, n_marbles)):
        possibilities[i] = factorial(g) / factorial(g - n) / factorial(n)
    print(possibilities[0] * possibilities[1])
    all_possibilities.append(possibilities[0] * possibilities[1])

fig, axe = plt.subplots()
axe.plot(all_possibilities, marker=".", linestyle="")

fig, axe = plt.subplots()
axe.plot(np.log(all_possibilities), marker=".", linestyle="")

plt.show()
