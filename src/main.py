from graph import (
    parse_equation,
    calculate_values,
    calculate_implicit_values,
    plot_all,
)


# Store equations entered by the user
equations = []

while True:
    equation = input("Enter an equation (or 'done' to finish): ")

    if equation.lower() == "done":
        break

    try:
        equation_data = parse_equation(equation)
        equations.append(equation_data)

    except ValueError as error:
        print(error)

if not equations:
    print("No equations entered.")
    exit()


# Graph settings
x_min = float(input("Enter x minimum: "))
x_max = float(input("Enter x maximum: "))
y_min = float(input("Enter y minimum: "))
y_max = float(input("Enter y maximum: "))
points = int(input("Enter number of points: "))

if x_min >= x_max:
    print("x minimum must be smaller than x maximum.")
    exit()

if y_min >= y_max:
    print("y minimum must be smaller than y maximum.")
    exit()

if points < 2:
    print("Number of points must be at least 2.")
    exit()

# Store calculated graph data
explicit_graphs = []
implicit_graphs = []


# Calculate each equation
for equation in equations:

    if equation.equation_type == "explicit":

        graph = calculate_values(
            equation.expression,
            equation.x,
            x_min,
            x_max,
            points
        )

        explicit_graphs.append(graph)

    else:
        graph = calculate_implicit_values(
        equation.expression,
        x_min,
        x_max,
        y_min,
        y_max,
        points
        )

        implicit_graphs.append(graph)


# Plot everything on the same graph
plot_all(
    explicit_graphs,
    implicit_graphs,
    y_min,
    y_max
)