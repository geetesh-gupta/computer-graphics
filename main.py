
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from utils.read_write import read_off_file
from common import MODEL_DETAILS, Models, Coords, FileDetails, Face
from model import Object

# Consider any one of the meshes and the corresponding camera location from the below table.
# Transform the object w.r.t. the camera coordinate system.
# Find oriented normal for each triangle.
# Determine the coordinates of the view frustum such that all the triangles lie in the view frustum.
# Perform the normalized device coordinate transformation (use inbuilt function for this purpose).
# TODO: Now, use the back-face culling algorithm to remove the invisible triangles.
# TODO: Place a light source at the locations specified.
# TODO: Use the Phong shading algorithm with highlights to find the intensity of at each pixel.
# TODO: Now, use any of the triangle rsterization algorithm to render the object.
# TODO: Determine the window and viewport sizes accordingly.
# TODO: Compare your results with the results obtained by using inbuilt functions to perform these steps.


if __name__ == '__main__':
    # Select model to use
    model = Models.triangle
    model_details = MODEL_DETAILS[model]
    file_path = model_details[FileDetails.FILE_PATH]
    camera_pos = model_details[FileDetails.CAMERA_POS]

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

    # Display some values
    print(f"World Coords: {obj.vertices[Coords.WORLD][:3]}")
    print(f"Camera Coords: {obj.vertices[Coords.CAMERA][:3]}")
    print("---Face 1---")
    for vertex_index, i in enumerate(obj.faces[Face.INDICES][0]):
        print(f"Vertex {i+1} World Coords: {obj.vertices[Coords.WORLD][vertex_index]}")
        print(f"Vertex {i+1} Camera Coords: {obj.vertices[Coords.CAMERA][vertex_index]}")
        print(f"Vertex {i+1} Normalized Coords: {obj.vertices[Coords.NORMALIZED][vertex_index]}")
    print(f"Face Normal: {obj.faces[Face.NORMAL][0]}")
    print("------------")
    print(f"View Frustum: {obj.view_frustum}")
