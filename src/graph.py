import numpy as np
import sympy as sp
from dataclasses import dataclass

@dataclass
class Equation:
    equation_type: str
    expression: sp.Expr
    x: sp.Symbol
    y: sp.Symbol

@dataclass
class GraphData:
    x_values: np.ndarray
    y_values: np.ndarray
    expression: sp.Expr

@dataclass
class ImplicitGraphData:
    X: np.ndarray
    Y: np.ndarray
    Z: np.ndarray
    expression: sp.Expr


from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)


transformations = standard_transformations + (
    convert_xor,
    implicit_multiplication_application,
)


def parse_equation(equation):
    x = sp.symbols("x")
    y = sp.symbols("y")

    try:

        # Equation contains =
        if "=" in equation:
            left_text, right_text = equation.split("=", 1)

            left = parse_expr(
                left_text,
                transformations=transformations
            )

            right = parse_expr(
                right_text,
                transformations=transformations
            )

            # y = f(x)
            if left == y and not right.has(y):
                return Equation(
                    "explicit",
                    right,
                    x,
                    y
                )

            # f(x) = y
            if right == y and not left.has(y):
                return Equation(
                    "explicit",
                    left,
                    x,
                    y
                )

            # Otherwise treat it as implicit
            expression = left - right

            return Equation(
                "implicit",
                expression,
                x,
                y
            )

        # No = sign
        expression = parse_expr(
            equation,
            transformations=transformations
        )

        # Contains y → implicit
        if expression.has(y):
            return Equation(
                "implicit",
                expression,
                x,
                y
            )

        # Only function of x
        return Equation(
            "explicit",
            expression,
            x,
            y
        )

    except (SyntaxError, TypeError, ValueError):
        raise ValueError("Invalid equation")

def calculate_values(expression, x, x_min, x_max, points):
    x_values = np.linspace(x_min, x_max, points)

    function = sp.lambdify(x, expression, "numpy")

    y_values = function(x_values)

    y_values = np.asarray(y_values, dtype=float)

    y_values[~np.isfinite(y_values)] = np.nan
    jumps = np.abs(np.diff(y_values))

    threshold = 100

    y_values[:-1][jumps > threshold] = np.nan
    y_values[1:][jumps > threshold] = np.nan

    return GraphData(
        x_values,
        y_values,
        expression
    )

def calculate_implicit_values(expression, x_min, x_max, y_min, y_max, points):
    x_values = np.linspace(x_min, x_max, points)
    y_values = np.linspace(y_min, y_max, points)

    X, Y = np.meshgrid(x_values, y_values)

    function = sp.lambdify(
        ("x", "y"),
        expression,
        "numpy"
    )

    Z = function(X, Y)

    return ImplicitGraphData(
    X,
    Y,
    Z,
    expression
)

import matplotlib.pyplot as plt


def plot_all(
    explicit_graphs,
    implicit_graphs,
    x_min,
    x_max,
    y_min,
    y_max
):
    fig, ax = plt.subplots(figsize=(9, 7))

    # Explicit equations
    for graph in explicit_graphs:
        ax.plot(
            graph.x_values,
            graph.y_values,
            label=f"y = {graph.expression}"
        )

    # Implicit equations
    for graph in implicit_graphs:
        contour = ax.contour(
            graph.X,
            graph.Y,
            graph.Z,
            levels=[0]
        )

        # Give implicit contours a legend label
        if contour.collections:
            contour.collections[0].set_label(
                f"{graph.expression} = 0"
            )

    # Coordinate axes
    ax.axhline(0)
    ax.axvline(0)

    # User-selected view
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    ax.grid(True)

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.set_aspect("equal", adjustable="box")
    ax.legend()

    plt.show()