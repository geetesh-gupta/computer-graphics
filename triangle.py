
def getTriangleMatrix(x0, y0, x1, y1, x2, y2, width, height, display_matrix, c=1):
    dx0 = x1-x0
    dx1 = x2-x1
    dx2 = x0-x2
    dy0 = y1-y0
    dy1 = y2-y1
    dy2 = y0-y2

    xmin = min(x0, x1, x2)
    xmax = max(x0, x1, x2)
    ymin = min(y0, y1, y2)
    ymax = max(y0, y1, y2)

    q = xmax-xmin
    f0 = (xmin-x0)*dy0 - (ymax-y0)*dx0
    f1 = (xmin-x1)*dy1 - (ymax-y1)*dx1
    f2 = (xmin-x2)*dy2 - (ymax-y2)*dx2

    g0 = (x0-x1)*dy1 - (y0-y1)*dx1
    g1 = (x1-x2)*dy2 - (y1-y2)*dx2
    g2 = (x2-x0)*dy0 - (y2-y0)*dx0

    # displayMatrix = [[0 for _ in range(int(width))]
    #                  for _ in range(int(height))]

    for y in range(ymax, ymin, -1):
        for x in range(xmin, xmax):
            alpha = f1/g1
            beta = f2/g2
            gamma = f0/g0
            if abs(1.0-(alpha + beta + gamma)) <= 0.00001 and 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1:
                display_matrix[height-y][x] = c
            f0 += dy0
            f1 += dy1
            f2 += dy2
        f0 -= q*dy0
        f1 -= q*dy1
        f2 -= q*dy2
        f0 += dx0
        f1 += dx1
        f2 += dx2
