import numpy as np


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
            if not np.all(np.isfinite(values)):
                continue

            epsilon = 1e-12

            sign_values = [
                epsilon if value == 0 else value
                for value in values
            ]
                
            crossings = {}

            for k in range(4):
                next_k = (k + 1) % 4

                v1 = values[k]
                v2 = values[next_k]

                if (sign_values[k] < 0) != (sign_values[next_k] < 0):
                    crossing = interpolate(
                        points[k],
                        points[next_k],
                        values[k],
                        values[next_k]
                    )

                    crossings[k] = crossing
            

            if len(crossings) == 2:
                p1, p2 = crossings.values()
                segments.append((p1, p2))
            elif len(crossings) == 4:
                center_value = sum(values) / 4

                if center_value >= 0:
                    if values[0] < 0:
                        edge_pairs = [(0, 3), (1, 2)]
                    else:
                        edge_pairs = [(0, 1), (2, 3)]
                else:
                    if values[0] > 0:
                        edge_pairs = [(0, 3), (1, 2)]
                    else:
                        edge_pairs = [(0, 1), (2, 3)]

                for edge1, edge2 in edge_pairs:
                    segments.append(
                        (crossings[edge1], crossings[edge2])
                    )

    return segments