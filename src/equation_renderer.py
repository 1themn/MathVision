import numpy as np


class EquationRenderer:
    def __init__(self, canvas, viewport):
        self.canvas = canvas
        self.viewport = viewport

    def draw_explicit(self, function):
        left, right, bottom, top = (
            self.viewport.get_visible_bounds()
        )

        x_values = np.linspace(left, right, 1000)
        y_values = function(x_values)

        points = []

        for x, y in zip(x_values, y_values):
            if not np.isfinite(y):
                continue

            screen_x, screen_y = (
                self.viewport.math_to_screen(x, y)
            )

            points.extend([screen_x, screen_y])

        if len(points) >= 4:
            self.canvas.create_line(
                *points,
                fill="#60a5fa",
                width=3,
                smooth=False
            )