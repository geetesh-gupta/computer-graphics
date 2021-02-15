from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 2, 10)
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


def Square(v0, v1, v2, v3):
    glBegin(GL_POLYGON)
    glVertex3fv(v0)
    glVertex3fv(v1)
    glVertex3fv(v2)
    glVertex3fv(v3)
    glEnd()


def Cube(v0, v1, v2, v3, v4, v5, v6, v7):
    glColor3f(1, 0, 0)
    Square(v0, v1, v2, v3)
    glColor3f(0, 1, 0)
    Square(v4, v5, v6, v7)
    glColor3f(0, 0, 1)
    Square(v0, v4, v7, v3)
    glColor3f(1, 1, 0)
    Square(v1, v5, v6, v2)
    glColor3f(1, 0, 1)
    Square(v3, v2, v7, v6)
    glColor3f(0, 1, 1)
    Square(v0, v1, v5, v4)


def draw():
    vertices = [
        [-0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5],
        [0.5, -0.5, 0.5],
        [-0.5, -0.5, 0.5],
        [-0.5, 0.5, -0.5],
        [0.5, 0.5, -0.5],
        [0.5, -0.5, -0.5],
        [-0.5, -0.5, -0.5],
    ]
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    # eyeX, eyeY, eyeZ, -> camera position
    # centerX, centerY, centerZ, -> camera looking towards this point
    # upX, upY, upZ -> camera's up vector
    gluLookAt(2, 3, 3, 0, 0, 0, 0, 1, 0)

    Cube(*vertices)

    glutSwapBuffers()


if __name__ == '__main__':
    main(draw)
