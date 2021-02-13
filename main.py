
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

MODELS = ['cat01', 'gorilla05', 'michael18', 'wolf02']
MODEL_DETAILS = {
    'cat01': {
        'file': 'PA2_Models/cat01.off',
        'camera': [-50, -60, 10],
        'light_source': [-50, -60, 160]
    },
    'gorilla05': {
        'file': 'PA2_Models/gorilla05.off',
        'camera': [-70, 30, 60],
        'light_source': [-70, 30, 60]
    },
    'michael18': {
        'file': 'PA2_Models/michael18.off',
        'camera': [-60, -120, 10],
        'light_source': [-60, -120, 80]
    },
    'wolf02': {
        'file': 'PA2_Models/wolf02.off',
        'camera': [-60, -120, 10],
        'light_source': [-60, -120, 100]
    },
}

# Consider any one of the meshes and the corresponding camera location from the below table.
# Transform the object w.r.t. the camera coordinate system.
# Find oriented normal for each triangle.
# Determinethe coordinates of the view frustum such that all the triangles lie in the view frustum.
# Perform the normalized device coordinate transformation (use inbuilt function for this purpose).
# Now, use the back-face culling algorithm to remove the invisible triangles.
# Place a light source at the locations specified.
# Use the Phong shading algorithm with highlights to find the intensity of at each pixel.
# Now, use any of the triangle rsterization algorithm to render the object.
# Determine the window and viewport sizes accordingly.
# Compare your results with the results obtained by using inbuilt functions to perform these steps.


def read_file(file):
    """
    returns 
    {
        num_vertices,
        num_faces,
        num_edges,
        vertices,
        faces,
    }
    """
    with open(file) as f:
        # First line: the letters OFF to mark the file type.
        filetype = f.readline()

        # Second line: the number of vertices, number of faces, and number of edges, in order
        num_vertices, num_faces, num_edges = list(
            map(int, f.readline().split()))

        # List of vertices: X, Y and Z coordinates
        vertices = []
        for _ in range(num_vertices):
            vertices.append(list(
                map(float, f.readline().split())))

        # List of faces: number of vertices, followed by the indexes of the composing vertices, in order (indexed from zero).
        faces = []
        for _ in range(num_faces):
            faces.append(list(
                map(int, f.readline().split()))[1:])

        return {
            'num_vertices': num_vertices,
            'num_faces': num_faces,
            'num_edges': num_edges,
            'vertices': vertices,
            'faces': faces,
        }


def convert_to_camera_coords(world_coords, camera_position):
    return [world_coords[i]-camera_position[i] for i in range(len(world_coords))]


class Object:
    def __init__(self, num_vertices, num_faces, num_edges, vertices, faces):
        self.num_vertices = num_vertices
        self.num_faces = num_faces
        self.num_edges = num_edges
        self.vertices = {
            'world_coords': vertices,
            'camera_coords': []
        }
        self.faces = faces

    def get_camera_coords(self, camera_position):
        self.vertices['camera_coords'] = [
            convert_to_camera_coords(v, camera_position) for v in self.vertices['world_coords']]

    def __str__(self):
        return f'Vertices: {self.num_vertices}, Faces: {self.num_faces}'


if __name__ == '__main__':
    # Select model to use
    model = MODELS[3]
    model_details = MODEL_DETAILS[model]

    # Create model object
    obj = Object(*read_file(model_details['file']).values())
    print(obj.vertices['world_coords'][:3])
    for vertex_index in obj.faces[0]:
        print(obj.vertices['world_coords'][vertex_index])

    # Get camera coordinates
    obj.get_camera_coords(model_details['camera'])
    print(obj.vertices['camera_coords'][:3])
    for vertex_index in obj.faces[0]:
        print(obj.vertices['camera_coords'][vertex_index])
