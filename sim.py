import numpy as np
from pathlib import Path
import os


def simulate(grid_shapes, marbles_per_grid, n_steps):
    tunnels = [(np.array((-1, 0, 0, 0)), np.array((4, 0, 0, 1))),  # format: x, y, z, grind
               (np.array((5, 0, 0, 1)), np.array((0, 0, 0, 0)))
               ]

    n_marbles = sum(marbles_per_grid)
    moves = np.array([[1, 0, 0, 0],
                      [-1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, -1, 0, 0]], dtype=np.int)

    occupations = [np.zeros(grid_shape, dtype=np.bool) for grid_shape in grid_shapes]

    for current_n_marbles, occupation in zip(marbles_per_grid, occupations):
        occupation.flat[np.random.choice(occupation.size, current_n_marbles, replace=False)] = 1

    trajectory = np.zeros((n_steps, n_marbles, len(grid_shapes[0]) + 1), dtype=np.int)
    all_locations = []
    for i, occupation in enumerate(occupations):
        locations = np.argwhere(occupation == 1)
        locations = np.concatenate((locations, i * np.ones((locations.shape[0], 1))), axis=1)
        all_locations.append(locations)

    trajectory[0] = np.concatenate(all_locations, axis=0)

    for step in range(1, n_steps):
        while True:
            selected_marble = np.random.choice(n_marbles)
            current_position = trajectory[step - 1, selected_marble]
            new_position = current_position + moves[np.random.choice(moves.shape[0])]

            for tunnel in tunnels:
                if np.array_equal(new_position, tunnel[0]):
                    new_position = tunnel[1]

            if np.all(new_position[:-1] < grid_shapes[new_position[-1]]) and \
                    np.all(new_position >= 0):
                if not occupations[new_position[-1]][tuple(new_position[:-1])]:
                    trajectory[step] = trajectory[step - 1]
                    trajectory[step, selected_marble] = new_position
                    occupations[current_position[-1]][tuple(current_position[:-1])] = False
                    occupations[new_position[-1]][tuple(new_position[:-1])] = True
                    break

    return trajectory


def run_path(path):
    """
    Creates a directory at "path/run{i}" where the i is corresponding to the smallest not yet existing path
    :param path: (str)
    :return: (str)
        path of the created folder
    """
    i = 0
    while True:
        current_path = os.path.join(path, "run{}".format(i))
        if not os.path.exists(current_path):
            os.makedirs(current_path)
            output_path = current_path
            break
        else:
            i += 1
    return Path(output_path)


if __name__ == "__main__":
    save_path = run_path(r"C:\Users\Tobias\coding\MarbleScience\004_EntropyCar\runs")
    grid_shapes = [(3, 3, 1), (5, 5, 1)]
    marbles_per_grid = [9, 0]
    n_marbles = sum(marbles_per_grid)
    n_steps = 1000
    trajectory = simulate(grid_shapes, marbles_per_grid, n_steps)
    np.save(save_path / "trajectory.npy", trajectory)
