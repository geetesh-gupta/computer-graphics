
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

DISPLAY_MATRIX = []
FACE_VERTICES = []
FACE_INTENSITIES = []
WINDOW_POS = [0, 0]
HEIGHT = 200
WIDTH = 200


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)


def main(func):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowPosition(*WINDOW_POS)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow("Pipeline")
    init()
    glutDisplayFunc(func)
    glutMainLoop()


def renderGLTriangle():
    glClear(GL_COLOR_BUFFER_BIT)
    for i in range(len(FACE_VERTICES)):
        # Set color
        pixelValue = FACE_INTENSITIES[i]
        curColorArr = [1.0, 0.0, 0.0]
        newColorArr = [k*pixelValue for k in curColorArr]
        glColor3f(newColorArr[0], newColorArr[1], newColorArr[2])

        # Draw triangle
        glBegin(GL_TRIANGLES)
        v1, v2, v3 = FACE_VERTICES[i]
        glVertex2f(*v1)
        glVertex2f(*v2)
        glVertex2f(*v3)
        glEnd()
    glFlush()


def renderUsingCustomFunction():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0, 0)
    glBegin(GL_POINTS)
    if len(DISPLAY_MATRIX) != 0:
        for i in range(HEIGHT):
            for j in range(WIDTH):
                pixelValue = DISPLAY_MATRIX[i][j]
                curColorArr = [1.0, 0.0, 0.0]
                newColorArr = [k*pixelValue for k in curColorArr]
                glColor3f(newColorArr[0], newColorArr[1], newColorArr[2])
                glVertex2f(j, HEIGHT-i)
    glEnd()
    glFlush()


if __name__ == '__main__':
    from utils.read_write import read_off_file
    from common import MODEL_DETAILS, Models, Coords, FileDetails, Face
    import numpy as np
    from pipeline import viewing_pipeline
    from face import rasterization, face_detection_and_shading, get_visible_face_coords

    # Cube
    model_enum = Models.cube
    camera_pos = np.array([0, 0, 1])
    light_source_pos = np.array([0, 0, 10])
    view_frustum = np.array([-5, 5, -5, 5, 2, 10])

    # Wolf
    # model_enum = Models.wolf02
    # camera_pos = np.array([0, 0, 100])
    # light_source_pos = np.array([0, 0, 100])
    # view_frustum = np.array([-20, 20, -20, 20, 2, 100])

    # Cat
    # model_enum = Models.cat01
    # camera_pos = np.array([0, 0, 150])
    # light_source_pos = np.array([0, 0, 150])
    # view_frustum = np.array([-20, 20, -40, 40, 2, 130])

    model_details = MODEL_DETAILS[model_enum]
    file_path = model_details[FileDetails.FILE_PATH]
    # camera_pos = model_details[FileDetails.CAMERA_POS]
    # light_source_pos = model_details[FileDetails.LIGHT_SOURCE_POS]
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
    # display_coords = rasterization(face_vertices, (WIDTH, HEIGHT))
    # DISPLAY_MATRIX = display_coords

    # Render openGL function
    main(renderGLTriangle)
