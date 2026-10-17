import numpy as np

from graph import calculate_values


class EquationRenderer:
    def __init__(self, canvas, viewport):
        self.canvas = canvas
        self.viewport = viewport

    def draw_explicit(self, equation, color="#60a5fa"):
        left, right, bottom, top = (
            self.viewport.get_visible_bounds()
        )

        points_count = max(
            1000,
            int(self.viewport.width)
        )

        graph = calculate_values(
            equation.expression,
            equation.x,
            left,
            right,
            points_count
        )

        segment = []

        def draw_segment():
            if len(segment) >= 4:
                self.canvas.create_line(
                    *segment,
                    fill=color,
                    width=2
                )

        for x, y in zip(
            graph.x_values,
            graph.y_values
        ):
            if not np.isfinite(y):
                draw_segment()
                segment = []
                continue

            screen_x, screen_y = (
                self.viewport.math_to_screen(
                    float(x),
                    float(y)
                )
            )

            # avoiding extremely large values.
            if not np.isfinite(screen_y):
                draw_segment()
                segment = []
                continue

            segment.extend([screen_x, screen_y])

        draw_segment()