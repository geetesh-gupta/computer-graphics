from common import Coords, Face
import numpy as np


class Object:
    def __init__(self, num_vertices, num_faces, num_edges, vertices, faces):
        self.num_vertices = num_vertices
        self.num_faces = num_faces
        self.num_edges = num_edges
        self.vertices = {
            Coords.WORLD: np.array(vertices),
            Coords.CAMERA: [],
            Coords.NORMALIZED: []
        }
        self.faces = {
            Face.INDICES: np.array(faces),
            Face.NORMAL: [],
            Face.VISIBLE: []
        }
        self.view_frustum = None

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
            self.faces[Face.NORMAL].append(normal)

    def get_view_frustum(self, camera_pos):
        l = float('inf')
        r = float('-inf')
        b = float('inf')
        t = float('-inf')
        n = camera_pos[2]+1
        f = float('-inf')
        for vertex in self.vertices[Coords.CAMERA]:
            x, y, z = vertex
            l = min(l, x)
            r = max(r, x)
            b = min(b, y)
            t = max(t, y)
            n = min(n, max(z, camera_pos[2]+1))
            f = max(f, z)
        # HACK: Workaround for zero sized frustum
        if f-n <= 0:
            f = n+1
        if r-l <= 0:
            r = l+1
        if t-b <= 0:
            t = b+1

        self.view_frustum = [l, r, b, t, n, f]

    def get_normalized_coords(self):
        l, r, b, t, n, f = self.view_frustum
        normalization_matrix = np.array([
            [2*n/(r-l), 0, (r+l)/(r-l), 0],
            [0, 2*n/(t-b), (t+b)/(t-b), 0],
            [0, 0, (n+f)/(n-f), 2*f*n/(n-f)],
            [0, 0, -1, 0]
        ])
        for v in self.vertices[Coords.CAMERA]:
            self.vertices[Coords.NORMALIZED].append(
                np.dot(normalization_matrix, [*v, 1])[:-1])

    def backface_detection(self, camera_direction):
        for face_normal in self.faces[Face.NORMAL]:
            self.faces[Face.VISIBLE].append(np.dot(
                camera_direction, face_normal) > 0)

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
