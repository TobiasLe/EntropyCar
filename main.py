import bpy
import numpy as np
from math import pi
from mathutils import Vector
# import pydevd_pycharm
# result = pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True)


def simulate(grid_shapes, marbles_per_grid, n_steps):
    tunnels = [(np.array((-1, 0, 0, 0)), np.array((0, 0, 0, 1))),
               (np.array((-1, 0, 0, 1)), np.array((0, 0, 0, 0)))]

    n_marbles = sum(marbles_per_grid)
    moves = np.array([[1, 0, 0, 0],
                      [-1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, -1, 0, 0]], dtype=np.int)

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


def add_collection(name, activate=True, clear=False):
    if name not in [c.name for c in bpy.data.collections]:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    else:
        collection = bpy.data.collections[name]

    if activate:
        layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
        bpy.context.view_layer.active_layer_collection = layer_collection

    if clear:
        while collection.objects:
            bpy.data.objects.remove(collection.objects[0])
    return collection


def create_grids(grid_shapes, grid_origins):
    grids = []
    for grid_shape, grid_origin in zip(grid_shapes, grid_origins):
        bpy.ops.mesh.primitive_plane_add(size=0.9, location=grid_origin)
        grid = bpy.context.active_object
        grid.modifiers.new("array_x", "ARRAY")
        grid.modifiers["array_x"].count = grid_shape[0]
        grid.modifiers["array_x"].use_constant_offset = True
        grid.modifiers["array_x"].use_relative_offset = False
        grid.modifiers["array_x"].constant_offset_displace = (1, 0, 0)

        grid.modifiers.new("array_y", "ARRAY")
        grid.modifiers["array_y"].count = grid_shape[1]
        grid.modifiers["array_y"].use_constant_offset = True
        grid.modifiers["array_y"].use_relative_offset = False
        grid.modifiers["array_y"].constant_offset_displace = (0, 1, 0)
        grids.append(grid)
    return grids


def create_marbles(n_marbles):
    marbles = []
    for i in range(n_marbles):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4)
        marble = bpy.context.active_object

        marble.animation_data_create()
        track_name = "main_track"
        if track_name in marble.animation_data.nla_tracks:
            main_track = marble.animation_data.nla_tracks[track_name]
        else:
            main_track = marble.animation_data.nla_tracks.new()
            main_track.name = track_name

        track_name = "motor_track"
        if track_name in marble.animation_data.nla_tracks:
            motor_track = marble.animation_data.nla_tracks[track_name]
        else:
            motor_track = marble.animation_data.nla_tracks.new()
            motor_track.name = track_name

        marbles.append(marble)
    return marbles


def grid_location(xyzg, grids):
    xyz = Vector(xyzg[:-1])
    if xyzg[-1] > 0:
        xyz += grids[xyzg[-1]].location
    return xyz


def main():
    grid_shapes = [(3, 3, 1), (5, 5, 1)]
    grid_origins = [(-3.12, -2.58, 1.74), (5, 5, 0)]
    marbles_per_grid = [9, 0]
    n_marbles = sum(marbles_per_grid)
    n_steps = 1000

    car_body = bpy.data.objects["car_body"]
    grids_collection = add_collection("grids", clear=True)
    grids = create_grids(grid_shapes, grid_origins)
    grids[0].rotation_euler = (pi / 2, 0, 0)

    grids[0].parent = car_body
    grids[1].parent = grids[0]

    # create marbles
    marbles_collection = add_collection("marbles", clear=True)
    marbles = create_marbles(n_marbles)
    for marble in marbles:
        marble.parent = grids[0]

    trajectory = simulate(grid_shapes, marbles_per_grid, n_steps)

    car_body.animation_data.action = None
    car_body.location[0] = 4.20
    car_body.keyframe_insert(data_path="location", frame=0)

    frame_i = 0
    for step_i in range(n_steps):
        for marble_i, marble in enumerate(marbles):
            grid_i = trajectory[step_i, marble_i, -1]

            if step_i > 0:
                delta_grid = grid_i-trajectory[step_i-1, marble_i, -1]
            else:
                delta_grid = 0

            if delta_grid == 0:
                marble.location = grid_location(trajectory[step_i, marble_i], grids)
                marble.keyframe_insert(data_path="location", frame=frame_i)

            elif delta_grid == 1:
                strip = marble.animation_data.nla_tracks["motor_track"].strips.new(name="sphere_action",
                                                                                   start=frame_i,
                                                                                   action=bpy.data.actions[
                                                                                       "SphereAction"])
                strip.blend_type = "ADD"
                car_body.keyframe_insert(data_path="location", frame=frame_i+13)
                car_body.location[0] += pi/2 * 1.326
                car_body.keyframe_insert(data_path="location", frame=frame_i+29)

                marble.keyframe_insert(data_path="location", frame=frame_i+45)
                marble.location = grid_location(trajectory[step_i, marble_i], grids)
                marble.keyframe_insert(data_path="location", frame=frame_i+50)
                frame_i += 50

            elif delta_grid == -1:
                strip = marble.animation_data.nla_tracks["motor_track"].strips.new(name="back_sphere_action",
                                                                                   start=frame_i,
                                                                                   action=bpy.data.actions[
                                                                                       "back_sphere_action"])
                strip.blend_type = "ADD"
                car_body.keyframe_insert(data_path="location", frame=frame_i + 13)
                car_body.location[0] -= pi/2 * 1.326
                car_body.keyframe_insert(data_path="location", frame=frame_i + 29)

                marble.keyframe_insert(data_path="location", frame=frame_i)
                marble.location = grid_location(trajectory[step_i, marble_i], grids)
                marble.keyframe_insert(data_path="location", frame=frame_i + 5)
                frame_i += 50
        frame_i += 3
    bpy.context.scene.frame_end = frame_i

    for marble in marbles:
        strip = marble.animation_data.nla_tracks["main_track"].strips.new(name="main_action", start=0, action=marble.animation_data.action)
        marble.animation_data.action = None
        strip.blend_type = "ADD"


main()
