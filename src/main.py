from graph import (
    parse_equation,
    calculate_values,
    calculate_implicit_values,
    plot_graph,
    plot_implicit,
)

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


explicit_equations = []
implicit_equations = []

for equation in equations:

    if equation.equation_type == "explicit":
        explicit_equations.append(
            (equation.expression, equation.x)
        )

    else:
        implicit_equations.append(
            equation.expression
        )



x_min = float(input("Enter x minimum: "))
x_max = float(input("Enter x maximum: "))
points = int(input("Enter number of points: "))
y_min = float(input("Enter y minimum: "))
y_max = float(input("Enter y maximum: "))



graphs = []

for expression, x in explicit_equations:
    graph = calculate_values(
        expression,
        x,
        x_min,
        x_max,
        points
    )

    graphs.append(graph)

if graphs:
    plot_graph(
        graphs,
        y_min,
        y_max
    )


for expression in implicit_equations:

    X, Y, Z = calculate_implicit_values(
        expression,
        x_min,
        x_max,
        y_min,
        y_max,
        points
    )

    plot_implicit(
        X,
        Y,
        Z,
        expression
    )

# print(equation_type)
# print(expression)


# graphs = []

# for x, expression in equations:
    

#     graphs.append(
#         calculate_values(
#             expression,
#             x,
#             x_min,
#             x_max,
#             points
#         )
#     )


# plot_graph(graphs, y_min, y_max)

# X, Y, Z = calculate_implicit_values(
#     expression,
#     -10,
#     10,
#     -10,
#     10,
#     500
# )

# plot_implicit(
#     X,
#     Y,
#     Z,
#     expression
# )
