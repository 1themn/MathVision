from graph import parse_equation, calculate_values, plot_graph


while True:
    equation = input("Enter an equation in x: ")

    try:
        x, expression = parse_equation(equation)
        break
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

x_values, y_values = calculate_values(
    expression,
    x,
    x_min,
    x_max,
    points
)

plot_graph(x_values, y_values, expression)