import os
import sys
import bpyplot
from math import pi
import numpy as np

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.append(cwd)
from setup_scene import *
from possibility_calc import number_of_permutations_on_grids

n_marbles = 9
car_delta_x = pi / 2 * 1.326
grid_shapes = [(3, 3, 1), (5, 5, 1)]

number_of_permutations = number_of_permutations_on_grids(n_marbles, [np.prod(g) for g in grid_shapes])
figure = bpyplot.Figure(shape=(10 * car_delta_x, 5 * car_delta_x))
figure.figure_origin.rotation_euler[0] = pi / 2
figure.figure_origin.location = [-0.5 * car_delta_x, 6.4, 9]
figure.bar_chart(number_of_permutations, set_extent=False, animated=False)

figure.axes[0].set_ticks(list(range(len(number_of_permutations))), [None] * len(number_of_permutations),
                         auto_toggle_visibility=False)
figure.axes[1].set_ticks([0, 5000000, 10000000, 15000000], auto_toggle_visibility=False)
figure.extent = [[-0.5, 9.5], [0, 18000000]]

figure2 = bpyplot.Figure(shape=(10 * car_delta_x, 5 * car_delta_x))
figure2.figure_origin.rotation_euler[0] = pi / 2
figure2.figure_origin.location = [-0.5 * car_delta_x, 6.4, 18]
figure2.bar_chart(np.log(number_of_permutations), set_extent=False, animated=False)
figure2.axes[0].set_ticks(list(range(len(number_of_permutations))), [None] * len(number_of_permutations),
                          auto_toggle_visibility=False)
figure2.axes[1].set_ticks([0, 5, 10, 15], auto_toggle_visibility=False)
figure2.extent = [[-0.5, 9.5], [0, 18]]
