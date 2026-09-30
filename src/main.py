from graph import parse_equation, calculate_values, plot_graph


equations = []

while True:
    equation = input("Enter an equation (or 'done' to finish): ")

    if equation.lower() == "done":
        break

    try:
        x, expression = parse_equation(equation)
        equations.append((x, expression))
    except ValueError as error:
        print(error)

x_min = float(input("Enter x minimum: "))
x_max = float(input("Enter x maximum: "))
points = int(input("Enter number of points: "))


try:
    x, expression = parse_equation(equation)
except ValueError as error:
    print(error)
    exit()

graphs = []

for x, expression in equations:
    x_values, y_values = calculate_values(
        expression,
        x,
        x_min,
        x_max,
        points
    )

    graphs.append((x_values, y_values, expression)) 

plot_graph(graphs)