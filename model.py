from utils.tranformations import transform_to_camera_coords
from common import Coords


class Object:
    def __init__(self, num_vertices, num_faces, num_edges, vertices, faces):
        self.num_vertices = num_vertices
        self.num_faces = num_faces
        self.num_edges = num_edges
        self.vertices = {
            Coords.WORLD: vertices,
            Coords.CAMERA: []
        }
        self.faces = faces

    def get_camera_coords(self, camera_position):
        self.vertices[Coords.CAMERA] = [
            transform_to_camera_coords(v, camera_position) for v in self.vertices[Coords.WORLD]]

    def __str__(self):
        return f'Vertices: {self.num_vertices}, Faces: {self.num_faces}'
