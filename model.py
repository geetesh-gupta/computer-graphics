from common import Coords, Face
import numpy as np


class Object:
    def __init__(self, num_vertices, num_faces, num_edges, vertices, faces):
        self.num_vertices = num_vertices
        self.num_faces = num_faces
        self.num_edges = num_edges
        self.vertices = {
            Coords.WORLD: np.array(vertices),
            Coords.CAMERA: []
        }
        self.faces = {
            Face.INDICES: np.array(faces),
            Face.NORMAL: []
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
        n = float(camera_pos[2])
        f = float('-inf')
        for vertex in self.vertices[Coords.CAMERA]:
            x, y, z = vertex
            l = min(l, x)
            r = max(r, x)
            b = min(b, y)
            t = max(t, y)
            n = min(n, z)
            f = max(f, z)
        # HACK: Workaround for zero sized frustum
        if f-n == 0:
            f = n+1
        if r-l == 0:
            r = l+1
        if t-b == 0:
            t = b+1
            
        self.view_frustum = [l, r, b, t, n, f]

    def __str__(self):
        return f'Vertices: {self.num_vertices}, Faces: {self.num_faces}'
