import os
import sys
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.append(cwd)
from setup_scene import *

print(os.getcwd())
# import pydevd_pycharm
# result = pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True)

trajectory_path = r"C:\Users\Tobias\coding\MarbleScience\004_EntropyCar\runs\run1\trajectory.npy"
trajectory = np.load(trajectory_path)

frame_i = 0
for marble_i, marble in enumerate(marbles):
    marble.location = grid_location(trajectory[0, marble_i], grids)
    marble.keyframe_insert(data_path="location", frame=0)

for step_i in range(1, len(trajectory)):
    for marble_i, marble in enumerate(marbles):
        grid_i = trajectory[step_i, marble_i, -1]
        delta_grid = grid_i - trajectory[step_i - 1, marble_i, -1]

        if delta_grid == 0:
            marble.keyframe_insert(data_path="location", frame=frame_i + 1)
            marble.location = grid_location(trajectory[step_i, marble_i], grids)
            marble.keyframe_insert(data_path="location", frame=frame_i + 4)

        else:
            marble.keyframe_insert(data_path="location", frame=frame_i + 5)
            marble.location = grid_location(trajectory[step_i, marble_i], grids)
            marble.keyframe_insert(data_path="location", frame=frame_i + 40)

            if delta_grid == 1:
                car_body.keyframe_insert(data_path="location", frame=frame_i + 18)
                car_body.location[0] += pi / 2 * 1.326 * delta_grid
                car_body.keyframe_insert(data_path="location", frame=frame_i + 24)
            if delta_grid == -1:
                car_body.keyframe_insert(data_path="location", frame=frame_i + 21)
                car_body.location[0] += pi / 2 * 1.326 * delta_grid
                car_body.keyframe_insert(data_path="location", frame=frame_i + 27)

            frame_i += 40

    frame_i += 5

scene.frame_end = frame_i
