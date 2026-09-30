from graph import parse_equation, calculate_values, plot_graph


equation = input("Enter an equation in x: ")

x_min = float(input("Enter x minimum: "))
x_max = float(input("Enter x maximum: "))
points = int(input("Enter number of points: "))


x, expression = parse_equation(equation)

x_values, y_values = calculate_values(
    expression,
    x,
    x_min,
    x_max,
    points
)

plot_graph(x_values, y_values, expression)