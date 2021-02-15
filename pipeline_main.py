from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

DISPLAY_MATRIX = []
FACE_VERTICES = []
FACE_INTENSITIES = []
WINDOW_POS = [0, 0]
HEIGHT = 500
WIDTH = 500


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)


def main(func):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowPosition(*WINDOW_POS)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow("Pipeline")
    glutReshapeFunc(reshape)
    init()
    glutDisplayFunc(func)
    glutMainLoop()


def render3D():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    glTranslatef(0.0, -0.4, -5.0)
    glColor3f(1.0, 0.0, 0.0)
    for i in range(len(FACE_VERTICES)):
        # Set color
        pixelValue = FACE_INTENSITIES[i]
        curColorArr = [1.0, 0.0, 0.0]
        newColorArr = [k*pixelValue for k in curColorArr]
        glColor3f(newColorArr[0], newColorArr[1], newColorArr[2])
        scale_factor = 50
        v1, v2, v3 = FACE_VERTICES[i]

        # Draw triangle
        glBegin(GL_TRIANGLES)
        glVertex3f(*v1/scale_factor)
        glVertex3f(*v2/scale_factor)
        glVertex3f(*v3/scale_factor)
        glEnd()

        # Draw mesh
        # glBegin(GL_LINES)
        # glVertex3f(*v1/scale_factor)
        # glVertex3f(*v2/scale_factor)
        # glEnd()
        # glBegin(GL_LINES)
        # glVertex3f(*v1/scale_factor)
        # glVertex3f(*v3/scale_factor)
        # glEnd()
        # glBegin(GL_LINES)
        # glVertex3f(*v2/scale_factor)
        # glVertex3f(*v3/scale_factor)
        # glEnd()

    glutSwapBuffers()


def reshape(width, height):
    if height == 0:
        height = 1
    aspect = width/height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, aspect, 0.1, 50.0)


if __name__ == '__main__':
    from utils.read_write import read_off_file
    from common import MODEL_DETAILS, Models, Coords, FileDetails, Face
    import numpy as np
    from pipeline import viewing_pipeline
    from face import rasterization, face_detection_and_shading, get_visible_face_coords

    # Cube
    # model_enum = Models.cube
    # camera_pos = np.array([0, 0, 1])
    # light_source_pos = np.array([0, 0, 10])
    # view_frustum = np.array([-5, 5, -5, 5, 2, 10])

    # Wolf
    model_enum = Models.wolf02
    view_frustum = np.array([-20, 20, -20, 20, 2, 100])

    # Cat
    # model_enum = Models.cat01
    # camera_pos = np.array([0, 0, 1])
    # light_source_pos = np.array([0, 0, 10])
    # view_frustum = np.array([-20, 20, -40, 40, 2, 130])

    model_details = MODEL_DETAILS[model_enum]
    file_path = model_details[FileDetails.FILE_PATH]
    camera_pos = model_details[FileDetails.CAMERA_POS]
    light_source_pos = model_details[FileDetails.LIGHT_SOURCE_POS]
    camera_direction = [0, 0, -1]

    # Create model object
    model = read_off_file(file_path)
    faces = np.array(model['faces'])
    vertices = np.array(model['vertices'])

    window_coords = viewing_pipeline(
        vertices, camera_pos, WINDOW_POS, (WIDTH, HEIGHT), view_frustum)

    [faces_visible, face_intensities] = face_detection_and_shading(
        faces, vertices, camera_pos, camera_direction, light_source_pos)
    [FACE_VERTICES, FACE_INTENSITIES] = get_visible_face_coords(
        faces_visible, window_coords, faces, face_intensities)

    # print(np.array(FACE_VERTICES))
    # print(np.array(FACE_INTENSITIES))

    # Render openGL function
    main(render3D)
