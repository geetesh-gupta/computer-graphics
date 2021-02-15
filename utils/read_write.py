def read_off_file(file):
    """
    Returns 
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
            v = list(map(float, f.readline().split()))
            vertices.append([*v[:-1], v[-1]])

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
