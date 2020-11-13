import os
import sys
import bpyplot
import math

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.append(cwd)
from setup_scene import *
from possibility_calc import number_of_permutations_on_grids

try:
    import pydevd_pycharm

    pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True, suspend=False)
except ConnectionRefusedError:
    print("Debug connection refused")


def permutations_on_grid(shape, number_of_objects):
    """
    Generates all permutations of indistinguishable objects on a grid
    Args:
        shape:
        number_of_objects:

    Returns:
        A trajectory with the shape (number_of_permutations, number_of_objects, number_of_grid_dimensions)
        as numpy array.

    """
    number_of_positions = np.prod(shape)
    results = np.arange(number_of_objects)
    results = np.expand_dims(results, axis=0)
    for i in range(number_of_objects):
        results = np.repeat(results, number_of_positions, axis=0)
        results[:, i] = np.tile(np.arange(number_of_positions), int(results.shape[0] / number_of_positions))

        # filter two objects at same location
        sorted_results = np.sort(results)
        mask = np.all(sorted_results[:, 1:] != sorted_results[:, :-1], axis=1)
        results = results[mask]
        sorted_results = sorted_results[mask]

        # filter duplicates
        _, indices = np.unique([tuple(row) for row in sorted_results], axis=0, return_index=True)
        results = results[indices]
        pass

    # convert to grid indices
    results = np.stack(np.unravel_index(results, shape), axis=-1)
    return results


max_frames = [20 * 30] * 2 + [10 * 30] * n_marbles
frames_per_iter = [1] * 2 + [0.5] + [0.1] * n_marbles
min_frames = 5 * 30
car_delta_x = pi / 2 * 1.326

grid_shapes = [s[:2] for s in grid_shapes]

car_frames = []
frame_i = 0
for x in range(n_marbles + 1):
# for x in range(7):
    print("x", x)
    marbles_per_grid = [n_marbles - x, x]
    all_permutations = [permutations_on_grid(grid_shapes[i], marbles_per_grid[i]) for i in range(len(grid_shapes))]
    print("done generating permutations")
    car_body.location[0] = x * car_delta_x
    car_body.keyframe_insert(data_path="location", frame=frame_i)
    car_frames.append(frame_i)

    iters = 0
    for i in range(len(all_permutations[0])):
        if iters > max_frames[x]:
            break
        for marble_i, marble in enumerate(marbles[x:]):
            marble.location = grid_location([*all_permutations[0][i, marble_i], 0, 0], grids)
            marble.keyframe_insert(data_path="location", frame=frame_i)

        frame_i += frames_per_iter[x]
        iters += frames_per_iter[x]
        for j in range(len(all_permutations[1])):
            if iters > max_frames[x]:
                break
            for marble_i, marble in enumerate(marbles[:x]):
                marble.location = grid_location([*all_permutations[1][j, marble_i], 0, 1], grids)
                marble.keyframe_insert(data_path="location", frame=frame_i)
            frame_i += frames_per_iter[x]
            iters += frames_per_iter[x]

    if frame_i - car_frames[-1] < min_frames:
        frame_i = car_frames[-1] + min_frames

    car_body.keyframe_insert(data_path="location", frame=frame_i)
    frame_i += 10

for marble in marbles:
    fcurves = marble.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'CONSTANT'

number_of_permutations = number_of_permutations_on_grids(n_marbles, [np.prod(g) for g in grid_shapes])
figure = bpyplot.Figure(shape=(11 * car_delta_x, 5 * car_delta_x))
figure.figure_origin.rotation_euler[0] = pi / 2
figure.figure_origin.location = [-0.5 * car_delta_x, 6.4, 9]
figure.bar_chart(number_of_permutations, set_extent=False, animated=True, frames=[[f, f + 90] for f in car_frames])

figure.axes[0].set_ticks(list(range(len(number_of_permutations))), [None] * len(number_of_permutations),
                         auto_toggle_visibility=False)
for tick in figure.axes[0].ticks:
    tick.scale[1] = 45
    tick.scale[0] = 0.5

ylim = max(number_of_permutations)
labels = []
for i in range(math.ceil(math.log10(ylim))):
    labels += [j * 10 ** i for j in range(20)]
labels = list(set(labels))
figure.axes[1].set_ticks(labels)

extent = [[-0.5, 10.5], [0, 1.1]]
for i, frames in enumerate(car_frames):
    figure.add_extent_keyframe(frames + 5, extent)
    extent[1][1] = max(number_of_permutations[:i + 1]) * 1.1
    figure.add_extent_keyframe(frames + 60, extent)

scene.frame_end = frame_i
