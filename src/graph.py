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
        if "=" in equation:
            left, right = equation.split("=", 1)

            expression = parse_expr(
                left,
                transformations=transformations
            ) - parse_expr(
                right,
                transformations=transformations
            )
        else:
            expression = parse_expr(
                equation,
                transformations=transformations
            )
    except (SyntaxError, TypeError, ValueError):
        raise ValueError("Invalid equation")

    if expression.has(y):
        return Equation("implicit", expression, x, y)

    return Equation("explicit", expression, x, y)

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


def plot_all(explicit_graphs, implicit_graphs, y_min, y_max):

    # Plot explicit equations
    for graph in explicit_graphs:
        plt.plot(
            graph.x_values,
            graph.y_values,
            label=f"y = {graph.expression}"
        )

    # Plot implicit equations
    for graph in implicit_graphs:
        plt.contour(
            graph.X,
            graph.Y,
            graph.Z,
            levels=[0]
        )

    plt.axhline(0)
    plt.axvline(0)

    plt.ylim(y_min, y_max)

    plt.grid(True)

    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()

    plt.show()