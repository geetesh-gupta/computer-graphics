
def transform_to_camera_coords(world_coords, camera_position):
    return [world_coords[i]-camera_position[i] for i in range(len(world_coords))]
