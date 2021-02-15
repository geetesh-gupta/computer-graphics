from common import Coords, Face
import numpy as np
from triangle import getTriangleMatrix


def homogeneous_coords(x, y, z):
    return np.array([x, y, z, 1])


def model_view_matrix(cx, cy, cz):
    return np.array([
        [1, 0, 0, -cx],
        [0, 1, 0, -cy],
        [0, 0, 1, -cz],
        [0, 0, 0, 1]
    ])


def normal_model_view_matrix(cx, cy, cz):
    return np.linalg.inv(model_view_matrix(cx, cy, cz)).transpose()


def projection_matrix(l, r, b, t, n, f):
    return np.array([
        [2*n/(r-l), 0, (r+l)/(r-l), 0],
        [0, 2*n/(t-b), (t+b)/(t-b), 0],
        [0, 0, (n+f)/(n-f), 2*f*n/(n-f)],
        [0, 0, -1, 0]
    ])


def normalized_device_coords(clip_coords):
    return np.array(clip_coords[:-1])/clip_coords[3]


def viewport_matrix(window_pos, window_size, depth_coords, ndc):
    x, y = window_pos
    w, h = window_size
    n, f = depth_coords
    return np.array([
        ndc[0]*w/2 + x+w/2,
        ndc[1]*h/2 + y+h/2,
        ndc[2]*(f-n)/2 + (f+n)/2
    ])


def coords_in_2d(x, y, z):
    return np.array([x, y])


def transform_vertex(object_coords, camera_coords, view_frustum, window_pos, window_size):
    x, y, z = object_coords
    cx, cy, cz = camera_coords
    l, r, b, t, n, f = view_frustum
    hc = homogeneous_coords(*object_coords)
    mvc = np.matmul(model_view_matrix(*camera_coords), hc.transpose())
    # pc = np.matmul(projection_matrix(*view_frustum), mvc)
    ndc = normalized_device_coords(mvc)
    # wc = viewport_matrix(window_pos, window_size, (n, f), ndc)
    # wc2d = coords_in_2d(*wc)
    # print("-------------")
    # print(object_coords)
    # print(hc)
    # print(mvc)
    # print(pc)
    # print(ndc)
    # print(wc)
    # print(wc2d)
    # print("-------------")
    return ndc


def get_eye_coords(object_coords, camera_coords):
    hc = homogeneous_coords(*object_coords)
    mvc = np.matmul(model_view_matrix(*camera_coords), hc.transpose())
    nc = normalized_device_coords(mvc)
    return nc


def viewing_pipeline(object_coords, camera_coords, window_pos, window_size, view_frustum):
    window_coords = []
    for i, vertex in enumerate(object_coords):
        window_coord = transform_vertex(
            vertex, camera_coords, view_frustum, window_pos, window_size)
        window_coords.append(window_coord)
    window_coords = np.array(window_coords)
    return window_coords


if __name__ == '__main__':
    from utils.read_write import read_off_file
    from common import MODEL_DETAILS, Models, Coords, FileDetails, Face

    # Select model to use
    model = Models.cube
    model_details = MODEL_DETAILS[model]
    file_path = model_details[FileDetails.FILE_PATH]
    camera_pos = model_details[FileDetails.CAMERA_POS]
    light_source_pos = model_details[FileDetails.LIGHT_SOURCE_POS]
    camera_direction = [0, 0, -1]

    # Create model object
    model = read_off_file(file_path)
    object_coords = np.array(model['vertices'])
    window_coords = viewing_pipeline(
        object_coords, camera_pos, (0, 0), (100, 100), [-5, 5, -5, 5, 2, 10])
    # print(window_coords)
