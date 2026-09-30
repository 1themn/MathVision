import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

equation = input("Enter an equation in x: ")

x_symbol = sp.symbols("x")

expression = sp.sympify(equation)

x_values = np.linspace(-10, 10, 100)

function = sp.lambdify(x_symbol, expression, "numpy")

y_values = function(x_values)

plt.plot(x_values, y_values)
plt.show()