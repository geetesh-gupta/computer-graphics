from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from utils.read_write import read_off_file


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-30, 30, -50, 50, 2, 130)
    glMatrixMode(GL_MODELVIEW)


def main(func):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(100, 150)
    glutInitWindowSize(400, 400)
    glutCreateWindow("Cat")
    init()
    glutDisplayFunc(func)
    glutMainLoop()


def draw():
    model = read_off_file('PA2_Models/cat01.off')
    vertices = model['vertices']
    faces = model['faces']
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    # eyeX, eyeY, eyeZ, -> camera position
    # centerX, centerY, centerZ, -> camera looking towards this point
    # upX, upY, upZ -> camera's up vector
    gluLookAt(0, 0, 100, 0, 0, 0, 0, 1, 0)

    for face in faces:
        glBegin(GL_TRIANGLES)
        for vertex_index in face:
            vertex = vertices[vertex_index]
            glVertex3f(*vertex)
        glEnd()

    glutSwapBuffers()


if __name__ == '__main__':
    main(draw)
