import numpy as np
from pipeline import normal_model_view_matrix, get_eye_coords, homogeneous_coords, normalized_device_coords
from triangle import getTriangleMatrix


def get_face_normals(faces, vertices, camera_coords):
    normals = []
    for face in faces:
        v = [(vertices[i]-camera_coords) for i in face]
        side1 = v[1] - v[0]
        side2 = v[2] - v[0]
        normal = np.cross(side1, side2)
        unit_normal = normal/np.linalg.norm(normal)
        normals.append(unit_normal)
    return np.array(normals)


def get_face_vertices(faces, vertices):
    face_vertices = []
    for face in faces:
        face_vertices.append([vertices[i] for i in face])
    return np.array(face_vertices)


def rasterization(face_vertices, window_size):
    display_matrix = np.zeros([window_size[1], window_size[0]], dtype=int)
    face_vertices = face_vertices.astype(int)
    for vertices in face_vertices:
        v1, v2, v3 = vertices
        getTriangleMatrix(*v1, *v2, *v3, *window_size, display_matrix, 1)
    return display_matrix


def backface_detection(camera_direction, faces_normals, face_eye_coords):
    visible_faces = []
    for i, vertices in enumerate(face_eye_coords):
        centroid = sum(vertices)/3
        face_normal = faces_normals[i]
        if np.dot(centroid - camera_direction, face_normal) < 0:
            visible_faces.append(True)
        else:
            visible_faces.append(False)
    return visible_faces


def apply_phong_shading(camera_direction, light_source_pos, face_normals, face_eye_coords):
    face_intensities = []
    for i, vertices in enumerate(face_eye_coords):
        centroid = sum(vertices)/3
        light_direction = -(centroid - light_source_pos)
        n = face_normals[i]
        l = light_direction / np.linalg.norm(light_direction)
        e = camera_direction/np.linalg.norm(camera_direction)
        h = (e+l)/np.linalg.norm(e+l)
        c = max(0, np.dot(n, l)) + np.dot(h, n)
        face_intensities.append(c)
    return face_intensities


def face_detection_and_shading(faces, vertices, camera_pos, camera_direction, light_source_pos):
    vertices = vertices - camera_pos
    face_vertices = get_face_vertices(faces, vertices)
    face_normals = get_face_normals(faces, vertices, camera_pos)
    faces_visible = backface_detection(
        camera_direction, face_normals, face_vertices)
    face_intensities = apply_phong_shading(
        camera_direction, light_source_pos, face_normals, face_vertices)
    return [faces_visible, face_intensities]


def get_visible_face_coords(faces_visible, vertices, faces, face_intensities):
    visible_faces_vertices = []
    visible_faces_intensities = []
    face_vertices = get_face_vertices(faces, vertices)
    for i, face_visible in enumerate(faces_visible):
        if face_visible:
            visible_faces_vertices.append(face_vertices[i])
            visible_faces_intensities.append(face_intensities[i])
    return [visible_faces_vertices, visible_faces_intensities]
