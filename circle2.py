import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import sqrt

"""
.   8   .   1   .
3   .   .   .   2
.   .   .   .   .
4   .   .   .   3
.   5   .   4   .
"""


def getQuad(x, y):
    if (x <= 0 and y >= 0 and -x < y):
        return 8
    elif (x < 0 and y > 0 and y <= -x):
        return 7
    elif (x < 0 and y <= 0 and -x > -y):
        return 6
    elif (x < 0 and y < 0 and -y >= -x):
        return 5
    elif (x >= 0 and y < 0 and x < -y):
        return 4
    elif (x >= 0 and y < 0 and -y <= x):
        return 3
    elif (x >= 0 and y >= 0 and x > y):
        return 2
    elif (x > 0 and y >= 0 and y >= x):
        return 1


def quad1(x, y, r):
    d = 5/4 - r/sqrt(2)
    while (getQuad(x, y) == 1):
        # print(d)
        if d <= 0:
            d = d + 2*x+3
            x -= 1
        else:
            d = d + 2*x-2*y+5
            x -= 1
            y += 1
        glVertex2f(x, y)


def quad2(x, y, r):
    d = 5/4 - 2*r
    while (getQuad(x, y) == 2):
        # print(d)
        if d <= 0:
            d = d + 2*y+3
            y += 1
        else:
            d = d - 2*x+2*y+5
            x -= 1
            y += 1
        glVertex2f(x, y)


def quad3(x, y, r):
    d = 5/4 + r/sqrt(2)
    while (getQuad(x, y) == 3):
        # print(d)
        if d <= 0:
            d = d - 2*y+3
            y += 1
        else:
            d = d - 2*x-2*y+5
            x += 1
            y += 1
        glVertex2f(x, y)


def quad4(x, y, r):
    d = 5/4 - r
    while (getQuad(x, y) == 4):
        # print(d)
        if d <= 0:
            d = d + 2*x+3
            x += 1
        else:
            d = d + 2*x+2*y+5
            x += 1
            y += 1
        glVertex2f(x, y)


def quad5(x, y, r):
    d = 5/4 - 3*r/sqrt(2)
    print(getQuad(x, y) == 5)
    while (getQuad(x, y) == 5):
        # print(d)
        if d <= 0:
            d = d - 2*x+3
            x += 1
        else:
            d = d - 2*x+2*y+5
            x += 1
            y -= 1
        print(x, y, getQuad(x, y))

        glVertex2f(x, y)


def quad6(x, y, r):
    d = 5/4 - 2*r
    while (getQuad(x, y) == 6):
        # print(d)
        if d <= 0:
            d = d - 2*y+3
            y -= 1
        else:
            d = d + 2*x-2*y+5
            x += 1
            y -= 1
        glVertex2f(x, y)


def quad7(x, y, r):
    d = 5/4 + r/sqrt(2)
    while (getQuad(x, y) == 7):
        # print(d)
        if d <= 0:
            d = d + 2*y+3
            y -= 1
        else:
            d = d + 2*x+2*y+5
            x -= 1
            y -= 1
        glVertex2f(x, y)


def quad8(x, y, r):
    d = 5/4 - r
    while (getQuad(x, y) == 8):
        # print(d)
        if d <= 0:
            d = d - 2*x+3
            x -= 1
        else:
            d = d - 2*x-2*y+5
            x -= 1
            y -= 1
        glVertex2f(x, y)


def drawCircle(x, y, r):

    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

    glBegin(GL_POINTS)

    if getQuad(x, y) == 1:
        quad1(x, y, r)
    elif getQuad(x, y) == 2:
        quad2(x, y, r)
    elif getQuad(x, y) == 3:
        quad3(x, y, r)
    elif getQuad(x, y) == 4:
        quad4(x, y, r)
    elif getQuad(x, y) == 5:
        quad5(x, y, r)
    elif getQuad(x, y) == 6:
        quad6(x, y, r)
    elif getQuad(x, y) == 7:
        quad7(x, y, r)
    elif getQuad(x, y) == 8:
        quad8(x, y, r)
    glEnd()


# def displayQuadsPartition(r):
#     midpoint_line(0, 0, -r, 0)
#     midpoint_line(0, 0, r, 0)
#     midpoint_line(0, 0, 0, -r)
#     midpoint_line(0, 0, 0, r)
#     midpoint_line(0, 0, -r/sqrt(2), r/sqrt(2))
#     midpoint_line(0, 0, -r/sqrt(2), -r/sqrt(2))
#     midpoint_line(0, 0, r/sqrt(2), -r/sqrt(2))
#     midpoint_line(0, 0, r/sqrt(2), r/sqrt(2))


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    radius = 400
    radius_sqrt = radius/sqrt(2)
    glColor3f(1.0, 1.0, 1.0)
    # displayQuadsPartition(radius)

    glColor3f(0.4, 0.9, 0.9)
    drawCircle(0, radius, radius)

    glColor3f(0.5, 0.1, 0.9)
    drawCircle(-radius_sqrt, radius_sqrt, radius)

    glColor3f(0.0, 0.9, 0.3)
    drawCircle(-radius, 0, radius)

    glColor3f(0.1, 0.5, 0.9)
    drawCircle(-radius_sqrt, -radius_sqrt, radius)

    glColor3f(0.7, 0.3, 0.3)
    drawCircle(0, -radius, radius)

    glColor3f(0.3, 0.5, 0.1)
    drawCircle(radius_sqrt, -radius_sqrt, radius)

    glColor3f(0.0, 0.3, 0.9)
    drawCircle(radius, 0, radius)

    glColor3f(0.8, 0.5, 0.7)
    drawCircle(radius_sqrt, radius_sqrt, radius)

    glFlush()


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-500, 500, -500, 500)


def main(func):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowPosition(10, 30)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Function Plotter")
    init()
    glutDisplayFunc(func)
    glutMainLoop()


if __name__ == "__main__":
    main(render)
