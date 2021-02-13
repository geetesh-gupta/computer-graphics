
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from utils.read_write import read_off_file
from common import MODEL_DETAILS, Models, Coords, FileDetails
from model import Object

# Consider any one of the meshes and the corresponding camera location from the below table.
# Transform the object w.r.t. the camera coordinate system.
# TODO: Find oriented normal for each triangle.
# TODO: Determinethe coordinates of the view frustum such that all the triangles lie in the view frustum.
# TODO: Perform the normalized device coordinate transformation (use inbuilt function for this purpose).
# TODO: Now, use the back-face culling algorithm to remove the invisible triangles.
# TODO: Place a light source at the locations specified.
# TODO: Use the Phong shading algorithm with highlights to find the intensity of at each pixel.
# TODO: Now, use any of the triangle rsterization algorithm to render the object.
# TODO: Determine the window and viewport sizes accordingly.
# TODO: Compare your results with the results obtained by using inbuilt functions to perform these steps.


if __name__ == '__main__':
    # Select model to use
    model = Models.wolf02
    model_details = MODEL_DETAILS[model]

    # Create model object
    obj = Object(*read_off_file(model_details[FileDetails.FILE_PATH]).values())

    # Get camera coordinates
    obj.get_camera_coords(model_details[FileDetails.CAMERA_POS])

    # Display some values
    print(obj.vertices[Coords.WORLD][:3])
    print(obj.vertices[Coords.CAMERA][:3])
    print("Face 1")
    for vertex_index in obj.faces[0]:
        print(f"World Coords: {obj.vertices[Coords.WORLD][vertex_index]}")
        print(f"Camera Coords: {obj.vertices[Coords.CAMERA][vertex_index]}")
