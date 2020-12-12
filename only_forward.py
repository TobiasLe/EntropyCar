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
    marble.keyframe_insert(data_path="location", frame=0)

for step_i in range(1, len(trajectory)):
    for marble_i, marble in enumerate(marbles):
        grid_i = trajectory[step_i, marble_i, -1]
        delta_grid = grid_i - trajectory[step_i - 1, marble_i, -1]

        if delta_grid == 0:
            # marble.keyframe_insert(data_path="location", frame=frame_i)
            marble.location = grid_location(trajectory[step_i, marble_i], grids)
            marble.keyframe_insert(data_path="location", frame=frame_i + 1)

        else:
            factor = 0.25
            marble.keyframe_insert(data_path="location", frame=frame_i + 5*factor)
            marble.location = grid_location(trajectory[step_i, marble_i], grids)
            marble.keyframe_insert(data_path="location", frame=frame_i + 40*factor)

            if delta_grid == 1:
                car_body.keyframe_insert(data_path="location", frame=frame_i + 18*factor)
                car_body.location[0] += car_delta_x * delta_grid
                car_body.keyframe_insert(data_path="location", frame=frame_i + 24*factor)
            if delta_grid == -1:
                car_body.keyframe_insert(data_path="location", frame=frame_i + 21*factor)
                car_body.location[0] += car_delta_x * delta_grid
                car_body.keyframe_insert(data_path="location", frame=frame_i + 27*factor)

            frame_i += 40*factor

    frame_i += 1

number_of_permutations = number_of_permutations_on_grids(n_marbles, [np.prod(g) for g in grid_shapes])
figure2 = bpyplot.Figure(shape=(10 * car_delta_x, 5 * car_delta_x))
figure2.figure_origin.rotation_euler[0] = pi / 2
figure2.figure_origin.location = [-0.5 * car_delta_x, 6.4, 18]
figure2.bar_chart(np.log(number_of_permutations), set_extent=False, animated=False)
figure2.axes[0].set_ticks(list(range(len(number_of_permutations))), [None] * len(number_of_permutations),
                          auto_toggle_visibility=False)
figure2.axes[1].set_ticks([0, 5, 10, 15], auto_toggle_visibility=False)
figure2.extent = [[-0.5, 9.5], [0, 18]]

scene.frame_end = frame_i
