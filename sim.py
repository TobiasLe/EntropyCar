import numpy as np


def simulate(grid_shapes, marbles_per_grid, n_steps):
    tunnels = [(np.array((grid_shapes[0][0]+1, 0, 0, 0)), np.array((0, 0, 0, 0))),
               (np.array((-1, 0, 0, 1)), np.array((0, 0, grid_shapes[0][2], 0)))]

    n_marbles = sum(marbles_per_grid)
    moves = np.array([[1, 0, 0, 0],
                      [-1, 0, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, -1, 0]], dtype=np.int)

    occupations = [np.zeros(grid_shape, dtype=np.bool) for grid_shape in grid_shapes]

    for current_n_marbles, occupation in zip(marbles_per_grid, occupations):
        occupation.flat[np.random.choice(occupation.size, current_n_marbles, replace=False)] = 1

    trajectory = np.zeros((n_steps, n_marbles, len(grid_shapes[0])+1), dtype=np.int)
    all_locations = []
    for i, occupation in enumerate(occupations):
        locations = np.argwhere(occupation == 1)
        locations = np.concatenate((locations, i*np.ones((locations.shape[0], 1))), axis=1)
        all_locations.append(locations)

    trajectory[0] = np.concatenate(all_locations, axis=0)

    for step in range(1, n_steps):
        while True:
            selected_marble = np.random.choice(n_marbles)
            current_position = trajectory[step-1, selected_marble]
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


if __name__ == "__main__":
    grid_shapes = [(3, 1, 3), (5, 1, 5)]
    grid_origins = [(0, 0, 0), (4, 0, 0)]
    marbles_per_grid = [8, 0]
    n_marbles = sum(marbles_per_grid)
    n_steps = 1000
    simulate(grid_shapes, marbles_per_grid, n_steps)
