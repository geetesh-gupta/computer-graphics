from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from utils.read_write import read_off_file
import numpy as np


# frustum = [-70, 70, -70, 70, 2, 100]
frustum = [-1, 1, -1, 1, 2, 10]


def get_normalized_coords(vertices):
    global frustum
    l, r, b, t, n, f = frustum
    normalization_matrix = np.array([
        [2*n/(r-l), 0, (r+l)/(r-l), 0],
        [0, 2*n/(t-b), (t+b)/(t-b), 0],
        [0, 0, (n+f)/(n-f), 2*f*n/(n-f)],
        [0, 0, -1, 0]
    ])
    # print(normalization_matrix)
    normalized_vertices = np.zeros([len(vertices), 3])
    for i, v in enumerate(vertices):
        clip_coords = np.dot(normalization_matrix,
                             np.array([*v, 1]))
        normalized_coords = clip_coords/clip_coords[3]
        normalized_vertices[i] = normalized_coords[:-1]
    return normalized_vertices


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(*frustum)
    glMatrixMode(GL_MODELVIEW)


def main(func):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(100, 150)
    glutInitWindowSize(400, 400)
    glutCreateWindow("Color Cube with Camera")
    init()
    glutDisplayFunc(func)
    glutMainLoop()


def draw():
    model = read_off_file('PA2_Models/wolf02.off')
    vertices = model['vertices']
    faces = model['faces']
    normalized_vertices = get_normalized_coords(vertices)
    # print(vertices)
    # print(normalized_vertices)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    # eyeX, eyeY, eyeZ, -> camera position
    # centerX, centerY, centerZ, -> camera looking towards this point
    # upX, upY, upZ -> camera's up vector
    # gluLookAt(50, 0, 100, 0, 0, 0, 0, 1, 0)
    # gluLookAt(0, 0, 50, 0, 0, 0, 0, 1, 0)
    # gluLookAt(0,0,50,0,0,1,0,1,0)
    gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)

    for face in faces:
        glBegin(GL_TRIANGLES)
        for vertex_index in face:
            # vertex = vertices[vertex_index]
            vertex = normalized_vertices[vertex_index]
            glVertex3f(*vertex)
        glEnd()

    glutSwapBuffers()


if __name__ == '__main__':
    main(draw)
