models = ['cat01', 'gorilla05', 'michael18', 'wolf02']
model_details = {
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


def readline(f):
    return list(map(float, f.readline().split()))


def read_file(file):
    with open(file) as f:
        # First line: the letters OFF to mark the file type.
        filetype = f.readline()

        # Second line: the number of vertices, number of faces, and number of edges, in order
        num_vertices, num_faces, num_edges = list(map(int, f.readline().split()))

        # List of vertices: X, Y and Z coordinates
        vertices = []
        for _ in range(num_vertices):
            vertices.append(readline(f))

        # List of faces: number of vertices, followed by the indexes of the composing vertices, in order (indexed from zero).
        faces = []
        for _ in range(num_faces):
            faces.append(readline(f)[1:])

        return {
            'num_vertices': num_vertices,
            'num_faces': num_faces,
            'num_edges': num_edges,
            'vertices': vertices,
            'faces': faces,
        }


print(read_file(model_details[models[0]]['file']))
