def interpolate(p1, p2, v1, v2):
    if v1 == v2:
        t = 0.5
    else:
        t = -v1 / (v2 - v1)

    return (
        p1[0] + t * (p2[0] - p1[0]),
        p1[1] + t * (p2[1] - p1[1])
    )


def marching_squares(X, Y, Z):
    segments = []

    rows, cols = Z.shape

    for i in range(rows - 1):
        for j in range(cols - 1):

            # Four corners of the current cell
            points = [
                (X[i, j], Y[i, j]),
                (X[i, j+1], Y[i, j+1]),
                (X[i+1, j+1], Y[i+1, j+1]),
                (X[i+1, j], Y[i+1, j])
            ]

            values = [
                Z[i, j],
                Z[i, j+1],
                Z[i+1, j+1],
                Z[i+1, j]
            ]

            crossings = []

            for k in range(4):
                next_k = (k + 1) % 4

                v1 = values[k]
                v2 = values[next_k]

                if (v1 < 0) != (v2 < 0):
                    crossing = interpolate(
                        points[k],
                        points[next_k],
                        v1,
                        v2
                    )

                    crossings.append(crossing)

            if len(crossings) == 2:
                segments.append(
                    (crossings[0], crossings[1])
                )

    return segments