import bpy
import numpy as np
from math import pi
from mathutils import Vector


# import pydevd_pycharm
# result = pydevd_pycharm.settrace('localhost', port=1090, stdoutToServer=True, stderrToServer=True)


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
    scene_path = r"X:\Google Drive\MarbleScience\projects\004_EntropyCar\scene.blend"
    trajectory_path = r"C:\Users\Tobias\coding\MarbleScience\004_EntropyCar\runs\run0\trajectory.npy"
    grid_shapes = [(3, 3, 1), (5, 5, 1)]
    grid_origins = [(-0.024158, -2.58, 0.714009), (-10.2217, 0, 0)]
    marbles_per_grid = [9, 0]
    n_marbles = sum(marbles_per_grid)
    n_steps = 1000

    trajectory = np.load(trajectory_path)

    with bpy.data.libraries.load(scene_path, link=False) as (data_from, data_to):
        data_to.scenes = data_from.scenes

    bpy.data.scenes.remove(bpy.context.scene)
    scene = bpy.context.scene
    scene.render.fps = 30
    scene.frame_end = n_steps

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

    car_body.animation_data.action = None
    car_body.location[0] = 4.20
    car_body.keyframe_insert(data_path="location", frame=0)

    frame_i = 0
    for marble_i, marble in enumerate(marbles):
        marble.location = grid_location(trajectory[0, marble_i], grids)
        marble.keyframe_insert(data_path="location", frame=0)

    for step_i in range(1, n_steps):
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

main()
