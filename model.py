from common import Coords, Face
import numpy as np
from triangle import getTriangleMatrix


class Object:
    def __init__(self, num_vertices, num_faces, num_edges, vertices, faces):
        self.num_vertices = num_vertices
        self.num_faces = num_faces
        self.num_edges = num_edges
        self.vertices = {
            Coords.WORLD: np.array(vertices),
            Coords.CAMERA: [],
            Coords.NORMALIZED: [],
            Coords.VIEWPORT: []
        }
        self.faces = {
            Face.INDICES: np.array(faces),
            Face.NORMAL: [],
            Face.VISIBLE: [True for _ in range(num_faces)],
            Face.LIGHT_INTENSITY: []
        }
        self.view_frustum = None
        self.within_range = num_vertices

    def get_camera_coords(self, camera_position):
        self.vertices[Coords.CAMERA] = self.vertices[Coords.WORLD] - \
            camera_position

    def get_face_normals(self):
        for face in self.faces[Face.INDICES]:
            vertices = [self.vertices[Coords.WORLD][vertex_index]
                        for vertex_index in face]
            side1 = vertices[1] - vertices[0]
            side2 = vertices[2] - vertices[0]
            normal = np.cross(side1, side2)
            unit_normal = normal/np.linalg.norm(normal)
            self.faces[Face.NORMAL].append(unit_normal)

    def get_view_frustum(self):
        l = float('inf')
        r = float('-inf')
        b = float('inf')
        t = float('-inf')
        n = float('-inf')
        f = float('inf')
        for vertex in self.vertices[Coords.CAMERA]:
            x, y, z = vertex
            r = max(r, abs(x))
            t = max(r, abs(y))
            f = max(r, abs(z))
        l = -r
        b = -t
        n = -1
        self.view_frustum = [l, r, b, t, n, f]

    def get_normalized_coords(self):
        l, r, b, t, n, f = self.view_frustum
        n = -n
        f = -f
        normalization_matrix = np.array([
            [2*n/(r-l), 0, (r+l)/(r-l), 0],
            [0, 2*n/(t-b), (t+b)/(t-b), 0],
            [0, 0, (n+f)/(n-f), 2*f*n/(n-f)],
            [0, 0, -1, 0]
        ])

        self.vertices[Coords.NORMALIZED] = np.zeros(
            [len(self.vertices[Coords.CAMERA]), 3])
        for i, v in enumerate(self.vertices[Coords.CAMERA]):
            clip_coords = np.dot(normalization_matrix,
                                 np.array([*v, 1]).transpose())
            normalized_coords = clip_coords/clip_coords[3]
            self.vertices[Coords.NORMALIZED][i] = (normalized_coords[:-1])

    def clip_triangles(self):
        for i, face in enumerate(self.faces[Face.INDICES]):
            for vertex_index in face:
                vertex = self.vertices[Coords.NORMALIZED][vertex_index]
                if not ((vertex >= -1).all() and (vertex <= 1).all()):
                    self.faces[Face.VISIBLE][i] = False
                    break

    def backface_detection(self, camera_direction):
        for i, face_normal in enumerate(self.faces[Face.NORMAL]):
            if self.faces[Face.VISIBLE][i]:
                self.faces[Face.VISIBLE][i] = np.dot(
                    camera_direction, face_normal) > 0

    def apply_phong_shading(self, camera_direction, light_source_pos):
        for i, face in enumerate(self.faces[Face.INDICES]):
            vertices = [self.vertices[Coords.CAMERA][vertex_index]
                        for vertex_index in face]
            centroid = sum(vertices)/3
            light_direction = (centroid - light_source_pos)
            n = self.faces[Face.NORMAL][i]
            l = light_direction / np.linalg.norm(light_direction)
            e = camera_direction/np.linalg.norm(camera_direction)
            h = (e+l)/np.linalg.norm(e+l)
            c = max(0, np.dot(n, l)) + np.dot(h, n)
            self.faces[Face.LIGHT_INTENSITY].append(c)

    def window_viewport_transformation(self, viewport):
        self.vertices[Coords.VIEWPORT] = np.zeros(
            [len(self.vertices[Coords.CAMERA]), 2], dtype=int)
        for i, face in enumerate(self.faces[Face.INDICES]):
            if self.faces[Face.VISIBLE][i]:
                for vertex_index in face:
                    v = self.vertices[Coords.NORMALIZED][vertex_index]
                    viewport_coords = [viewport[0] *
                                       (v[0]+1)/2, viewport[1]*(v[1]+1)/2]
                    self.vertices[Coords.VIEWPORT][vertex_index] = viewport_coords

    def get_display_coords(self, viewport):
        display_matrix = np.zeros([viewport[1], viewport[0]])
        for i, face in enumerate(self.faces[Face.INDICES]):
            if self.faces[Face.VISIBLE][i]:
                vertices = [self.vertices[Coords.VIEWPORT][vertex_index]
                            for vertex_index in face]
                v1, v2, v3 = vertices
                getTriangleMatrix(
                    *v1, *v2, *v3, *viewport, display_matrix, self.faces[Face.LIGHT_INTENSITY][i])
        return display_matrix

    def __str__(self):
        return f'Vertices: {self.num_vertices}, Faces: {self.num_faces}'


if __name__ == '__main__':
    from utils.read_write import read_off_file
    from common import MODEL_DETAILS, Models, Coords, FileDetails, Face
    from model import Object

    # Select model to use
    model = Models.triangle
    model_details = MODEL_DETAILS[model]
    file_path = model_details[FileDetails.FILE_PATH]
    camera_pos = model_details[FileDetails.CAMERA_POS]
    light_source_pos = model_details[FileDetails.LIGHT_SOURCE_POS]
    camera_direction = [0, 0, -1]

    # Create model object
    obj = Object(*read_off_file(file_path).values())

    # Get camera coordinates
    obj.get_camera_coords(camera_pos)

    # Get face normals
    obj.get_face_normals()

    # Get View frustum
    obj.get_view_frustum(camera_pos)

    # Get Normalized Coords
    obj.get_normalized_coords()

    # Backface Detection
    obj.backface_detection(camera_direction)

    # Display some values
    print(f"World Coords: {obj.vertices[Coords.WORLD][:3]}")
    print(f"Camera Coords: {obj.vertices[Coords.CAMERA][:3]}")
    print("---Face 1---")
    for vertex_index, i in enumerate(obj.faces[Face.INDICES][0]):
        print(
            f"Vertex {i+1} World Coords: {obj.vertices[Coords.WORLD][vertex_index]}")
        print(
            f"Vertex {i+1} Camera Coords: {obj.vertices[Coords.CAMERA][vertex_index]}")
        print(
            f"Vertex {i+1} Normalized Coords: {obj.vertices[Coords.NORMALIZED][vertex_index]}")
    print(f"Face Normal: {obj.faces[Face.NORMAL][0]}")
    print("------------")
    print(f"View Frustum: {obj.view_frustum}")
    print(f"Faces Visible: {obj.faces[Face.VISIBLE][:10]}")
