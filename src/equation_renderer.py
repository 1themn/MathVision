import numpy as np
from graph import calculate_implicit_values
from marching_squares import marching_squares

from graph import calculate_values


class EquationRenderer:
    def __init__(self, canvas, viewport):
        self.canvas = canvas
        self.viewport = viewport


    def draw_implicit(self, equation, color="#60a5fa"):
        left, right, bottom, top = (
            self.viewport.get_visible_bounds()
        )

        graph = calculate_implicit_values(
            equation.expression,
            left,
            right,
            bottom,
            top,
            200
        )

        segments = marching_squares(
            graph.X,
            graph.Y,
            graph.Z
        )

        for p1, p2 in segments:
            x1, y1 = self.viewport.math_to_screen(*p1)
            x2, y2 = self.viewport.math_to_screen(*p2)

            self.canvas.create_line(
                x1, y1,
                x2, y2,
                fill=color,
                width=2
            )


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
        previous_y = None

        max_jump = self.viewport.height

        def draw_segment():
            if len(segment) >= 4:
                self.canvas.create_line(
                    *segment,
                    fill=color,
                    width=2
                )

        for x, y in zip(graph.x_values, graph.y_values):

            if not np.isfinite(y):
                draw_segment()
                segment = []
                previous_y = None
                continue

            screen_x, screen_y = self.viewport.math_to_screen(
                float(x),
                float(y)
            )

            if not np.isfinite(screen_y):
                draw_segment()
                segment = []
                previous_y = None
                continue

            if previous_y is not None:
                if abs(screen_y - previous_y) > max_jump:
                    draw_segment()
                    segment = []

            segment.extend([screen_x, screen_y])

            previous_y = screen_y

        draw_segment()