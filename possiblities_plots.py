import os
import sys
import math
import bpyplot

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.append(cwd)
from setup_scene import *
from possibility_calc import number_of_permutations_on_grids

print(os.getcwd())
# import pydevd_pycharm
# result = pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True)

trajectory_path = r"C:\Users\Tobias\coding\MarbleScience\004_EntropyCar\runs\only_forward_run\trajectory.npy"
trajectory = np.load(trajectory_path)

car_delta_x = pi / 2 * 1.326

frame_i = 0
for marble_i, marble in enumerate(marbles):
    marble.location = grid_location(trajectory[0, marble_i], grids)

factor = 16
n_marbles = 9*factor
grid_spaces = [9*factor, 25*factor]
# n_marbles = 9*16
# grid_spaces = [9*16, 25*16]

# expo = 6
# expo = 31
expo = 133
number_of_permutations = np.array(number_of_permutations_on_grids(n_marbles, grid_spaces))
data = np.stack((np.arange(len(number_of_permutations))/factor, number_of_permutations/ 10**expo), axis=1)
figure2 = bpyplot.Figure(shape=(10 * car_delta_x, 5 * car_delta_x))
figure2.figure_origin.rotation_euler[0] = pi / 2
figure2.figure_origin.location = [-0.5 * car_delta_x, 6.4, 7.66]
figure2.bar_chart(data, set_extent=False, animated=False, bar_width=0.3/factor)
# figure2.axes[0].set_ticks(data[:, 0], [None] * len(number_of_permutations),
#                           auto_toggle_visibility=False)
figure2.axes[1].set_latex_label(r"Possibilities $\Omega$")
# figure2.axes[1].set_ticks([0, 5, 10, 15], auto_toggle_visibility=False)
# figure2.extent = [[-0.5, 9.5], [0, 18]]
figure2.axes[1].set_ticks([0, 5, 10], auto_toggle_visibility=False)
figure2.extent = [[-0.5, 9.5], [0, 12]]

exponent = bpyplot.latex_text(r"$\cdot10^{" + str(expo) + r"}$", "exponent")
exponent.parent = figure2.figure_origin
exponent.location[1] = 10
exponent.scale *= 1.5
bpy.data.objects["Camera"].location[2] = 13.642

bpy.data.objects["start_mark.001"].modifiers["Array"].count = factor * 9 + 1
bpy.data.objects["start_mark.001"].modifiers["Array"].constant_offset_displace[0] = car_delta_x / factor

bpy.data.objects["Plane"].modifiers["array_x"].count = 3 * int(factor**0.5)
bpy.data.objects["Plane"].modifiers["array_y"].count = 3 * int(factor**0.5)
bpy.data.objects["Plane"].scale /= int(factor**0.5)

bpy.data.objects["Plane.001"].modifiers["array_x"].count = 5 * int(factor**0.5)
bpy.data.objects["Plane.001"].modifiers["array_y"].count = 5 * int(factor**0.5)

scene.frame_end = frame_i
