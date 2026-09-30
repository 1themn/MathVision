import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

x_min = float(input("Enter x minimum: "))
x_max = float(input("Enter x maximum: "))
points = int(input("Enter number of points: "))

x = np.linspace(x_min, x_max, points)
print(x)

# equation = "log(x)"
# 
equation = input("Enter an equation in x: ")
x_symbol = sp.symbols("x")

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

transformations = standard_transformations + (
    implicit_multiplication_application,
)

try:
    expression = parse_expr(
        equation,
        transformations=transformations
    )

    x_values = np.linspace(-10, 10, 100)

    function = sp.lambdify(x_symbol, expression, "numpy")

    y_values = function(x_values)

    y_values = np.asarray(y_values, dtype=float)

    y_values[~np.isfinite(y_values)] = np.nan

    jumps = np.abs(np.diff(y_values))

    threshold = 100

    y_values[:-1][jumps > threshold] = np.nan
    y_values[1:][jumps > threshold] = np.nan
    valid = np.isfinite(y_values)

    x_values = x_values[valid]
    y_values = y_values[valid]
    
    print(y_values)

except Exception:
    print("Invalid equation. Please try again.")
    exit()



plt.plot(x_values, y_values)

plt.axhline(0)
plt.axvline(0)

plt.grid(True)

plt.xlabel("x")
plt.ylabel("y")

plt.title(f"y = {expression}")

plt.show()