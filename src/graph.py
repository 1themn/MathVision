import numpy as np
import sympy as sp

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

    expression = parse_expr(
        equation,
        transformations=transformations
    )

    return x, expression

def calculate_values(expression, x, x_min, x_max, points):
    x_values = np.linspace(x_min, x_max, points)

    function = sp.lambdify(x, expression, "numpy")

    y_values = function(x_values)

    y_values = np.asarray(y_values, dtype=float)

    y_values[~np.isfinite(y_values)] = np.nan

    return x_values, y_values


import matplotlib.pyplot as plt


def plot_graph(x_values, y_values, expression):
    plt.plot(x_values, y_values)

    plt.axhline(0)
    plt.axvline(0)

    plt.grid(True)

    plt.xlabel("x")
    plt.ylabel("y")

    plt.title(f"y = {expression}")

    plt.show()