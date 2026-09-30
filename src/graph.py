import numpy as np
import sympy as sp
from dataclasses import dataclass


@dataclass
class GraphData:
    x_values: np.ndarray
    y_values: np.ndarray
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

    try: 
        expression = parse_expr(
            equation,
            transformations=transformations
        )
    except (SyntaxError, TypeError, ValueError):
        raise ValueError("Invalid equation")

    return x, expression

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


import matplotlib.pyplot as plt


def plot_graph(graphs):
    all_y_values = []

    for graph in graphs:
        plt.plot(
            graph.x_values,
            graph.y_values,
            label=f"y = {graph.expression}"
        )

        valid_y = graph.y_values[np.isfinite(graph.y_values)]
        all_y_values.extend(valid_y)

    if all_y_values:
        y_min = min(all_y_values)
        y_max = max(all_y_values)

        padding = (y_max - y_min) * 0.05

        plt.ylim(
            y_min - padding,
            y_max + padding
        )

    plt.axhline(0)
    plt.axvline(0)

    plt.grid(True)

    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()

    plt.show()