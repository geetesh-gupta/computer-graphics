
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from utils.read_write import read_off_file
from common import MODEL_DETAILS, Models, Coords, FileDetails, Face
from model import Object
from scene import Scene

# Consider any one of the meshes and the corresponding camera location from the below table.
# Transform the object w.r.t. the camera coordinate system.
# Find oriented normal for each triangle.
# Determine the coordinates of the view frustum such that all the triangles lie in the view frustum.
# Perform the normalized device coordinate transformation (use inbuilt function for this purpose).
# Now, use the back-face culling algorithm to remove the invisible triangles.
# Place a light source at the locations specified.
# Use the Phong shading algorithm with highlights to find the intensity of at each pixel.
# Now, use any of the triangle rsterization algorithm to render the object.
# Determine the window and viewport sizes accordingly.
# TODO: Compare your results with the results obtained by using inbuilt functions to perform these steps.


DISPLAY_MATRIX = []
HEIGHT = 300
WIDTH = 300


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    # gluOrtho2D(-WIDTH, WIDTH, -HEIGHT, HEIGHT)
    # glOrtho(0, WIDTH, 0, HEIGHT, 1 ,100)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    # glOrtho(-200, 200, -200, 200, 1, 1000)


def main(func):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowPosition(10, 30)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow("Display Mesh")
    init()
    glutDisplayFunc(func)
    glutMainLoop()


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    if len(DISPLAY_MATRIX) != 0:
        for i in range(HEIGHT):
            for j in range(WIDTH):
                # Get the averaged pixel value
                pixelValue = DISPLAY_MATRIX[i][j]

                # Red Colored Triangle
                curColorArr = [1.0, 0.0, 0.0]

                # Modify color values based on averaged pixel value
                newColorArr = [k*pixelValue for k in curColorArr]

                # Set the color of the pixels
                glColor3f(newColorArr[0], newColorArr[1], newColorArr[2])

                # Draw the vertex
                glVertex2i(j, HEIGHT-i)
    glEnd()
    glFlush()


if __name__ == '__main__':
    # Select model to use
    model = Models.cube
    model_details = MODEL_DETAILS[model]
    file_path = model_details[FileDetails.FILE_PATH]
    camera_pos = model_details[FileDetails.CAMERA_POS]
    light_source_pos = model_details[FileDetails.LIGHT_SOURCE_POS]
    camera_direction = [0, 0, -1]

    # Create model object
    obj = Object(*read_off_file(file_path).values())
    scene = Scene(camera_pos, camera_direction,
                  light_source_pos, (WIDTH, HEIGHT))
    scene.add_object(obj)
    scene.simulate_model()
    DISPLAY_MATRIX = scene.display_coords

    # Display some values
    for coord in Coords:
        print(f"{str(coord)}:\n{obj.vertices[coord]}")
    print(f"View Frustum: {obj.view_frustum}")
    for j, face in enumerate(obj.faces[Face.INDICES]):
        print(f"-----Face {j+1}-----")
        print(f"Normal: {obj.faces[Face.NORMAL][j]}")
        print(f"Visible: {obj.faces[Face.VISIBLE][j]}")
        print(f"Intensity: {obj.faces[Face.LIGHT_INTENSITY][j]}")
        for i, vertex_index in enumerate(obj.faces[Face.INDICES][0]):
            print(f"Vertex {chr(ord('A')+vertex_index)}")
            print(
                f"\tWorld Coords: {obj.vertices[Coords.WORLD][vertex_index]}")
            print(
                f"\tCamera Coords: {obj.vertices[Coords.CAMERA][vertex_index]}")
            print(
                f"\tNormalized Coords: {obj.vertices[Coords.NORMALIZED][vertex_index]}")
    print("------------")
    # print(f"Faces Visible:\n{obj.faces[Face.VISIBLE]}")
    # print(f"Phong Shading Intensity: {obj.faces[Face.LIGHT_INTENSITY]}")
    # print(f"Display Coords:\n{scene.display_coords}")
    # print("------------")

    # import numpy as np
    # np.savetxt('out/WorldCoords.txt', obj.vertices[Coords.WORLD], fmt='%10.5f')
    # np.savetxt('out/CameraCoords.txt',
    #            obj.vertices[Coords.CAMERA], fmt='%10.5f')
    # np.savetxt('out/NormalizedCoords.txt',
    #            obj.vertices[Coords.NORMALIZED], fmt='%10.5f')
    # np.savetxt('out/ViewportCoords.txt',
    #            obj.vertices[Coords.VIEWPORT], fmt='%10.5f')
    # np.savetxt('out/VisibleFaces.txt', obj.faces[Face.VISIBLE], fmt='%1i')

    # Render openGL function
    # main(render)
