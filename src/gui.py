import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph import (
    parse_equation,
    calculate_values,
    calculate_implicit_values,
)


# =========================================================
# APP STATE
# =========================================================

root = tk.Tk()

root.title("MathVision")
root.geometry("1000x700")

equations = []


# =========================================================
# FUNCTIONS
# =========================================================

def add_equation():
    equation_text = equation_entry.get()

    if not equation_text.strip():
        return

    try:
        equation = parse_equation(equation_text)

        visible = tk.BooleanVar(value=True)

        equation_data = {
            "equation": equation,
            "text": equation_text,
            "visible": visible
        }

        equations.append(equation_data)

        create_equation_row(equation_data)

        equation_entry.delete(0, tk.END)

        plot_equations()

    except ValueError:
        print("Invalid equation")


def create_equation_row(equation_data):
    row = tk.Frame(equation_frame)

    row.pack(
        fill=tk.X,
        pady=2
    )

    checkbox = tk.Checkbutton(
        row,
        variable=equation_data["visible"],
        command=plot_equations
    )

    checkbox.pack(side=tk.LEFT)

    label = tk.Label(
        row,
        text=equation_data["text"]
    )

    label.pack(
        side=tk.LEFT,
        fill=tk.X,
        expand=True
    )

    remove_button = tk.Button(
        row,
        text="×",
        command=lambda: remove_equation(
            equation_data,
            row
        )
    )

    remove_button.pack(side=tk.RIGHT)


def remove_equation(equation_data, row):
    equations.remove(equation_data)

    row.destroy()

    plot_equations()


def update_range(event=None):
    try:
        plot_equations()

    except ValueError:
        pass


def plot_equations():
    ax.clear()

    if not equations:
        canvas.draw()
        return

    x_min = float(x_min_entry.get())
    x_max = float(x_max_entry.get())

    y_min = float(y_min_entry.get())
    y_max = float(y_max_entry.get())

    points = 1000

    for equation_data in equations:

        # Skip hidden equations
        if not equation_data["visible"].get():
            continue

        equation = equation_data["equation"]

        # Explicit equation
        if equation.equation_type == "explicit":

            graph = calculate_values(
                equation.expression,
                equation.x,
                x_min,
                x_max,
                points
            )

            ax.plot(
                graph.x_values,
                graph.y_values,
                label=equation_data["text"]
            )

        # Implicit equation
        else:

            graph = calculate_implicit_values(
                equation.expression,
                x_min,
                x_max,
                y_min,
                y_max,
                points
            )

            ax.contour(
                graph.X,
                graph.Y,
                graph.Z,
                levels=[0]
            )

    # Coordinate axes
    ax.axhline(0)
    ax.axvline(0)

    # Graph range
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Graph appearance
    ax.grid(True)

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.set_aspect(
        "equal",
        adjustable="box"
    )

    ax.legend()

    canvas.draw()


# =========================================================
# MAIN LAYOUT
# =========================================================

sidebar = tk.Frame(
    root,
    width=280
)

sidebar.pack(
    side=tk.LEFT,
    fill=tk.Y,
    padx=10,
    pady=10
)


graph_frame = tk.Frame(root)

graph_frame.pack(
    side=tk.RIGHT,
    fill=tk.BOTH,
    expand=True
)


# =========================================================
# EQUATION CONTROLS
# =========================================================

equation_label = tk.Label(
    sidebar,
    text="Equation"
)

equation_label.pack(
    anchor="w"
)


equation_entry = tk.Entry(
    sidebar,
    width=30
)

equation_entry.pack(
    fill=tk.X,
    pady=(5, 5)
)


add_button = tk.Button(
    sidebar,
    text="Add Equation",
    command=add_equation
)

add_button.pack(
    fill=tk.X
)


# Press Enter to add equation
equation_entry.bind(
    "<Return>",
    lambda event: add_equation()
)


# Container for equation rows
equation_frame = tk.Frame(sidebar)

equation_frame.pack(
    fill=tk.X,
    pady=10
)


# =========================================================
# GRAPH RANGE CONTROLS
# =========================================================

range_frame = tk.LabelFrame(
    sidebar,
    text="Graph Range"
)

range_frame.pack(
    fill=tk.X,
    pady=20
)


# X Min
tk.Label(
    range_frame,
    text="X Min"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

x_min_entry = tk.Entry(
    range_frame,
    width=8
)

x_min_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# X Max
tk.Label(
    range_frame,
    text="X Max"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

x_max_entry = tk.Entry(
    range_frame,
    width=8
)

x_max_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# Y Min
tk.Label(
    range_frame,
    text="Y Min"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)

y_min_entry = tk.Entry(
    range_frame,
    width=8
)

y_min_entry.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)


# Y Max
tk.Label(
    range_frame,
    text="Y Max"
).grid(
    row=3,
    column=0,
    padx=5,
    pady=5
)

y_max_entry = tk.Entry(
    range_frame,
    width=8
)

y_max_entry.grid(
    row=3,
    column=1,
    padx=5,
    pady=5
)


# Default ranges
x_min_entry.insert(0, "-10")
x_max_entry.insert(0, "10")

y_min_entry.insert(0, "-10")
y_max_entry.insert(0, "10")


# Press Enter to update graph range
x_min_entry.bind("<Return>", update_range)
x_max_entry.bind("<Return>", update_range)

y_min_entry.bind("<Return>", update_range)
y_max_entry.bind("<Return>", update_range)


# =========================================================
# MATPLOTLIB GRAPH
# =========================================================

figure = Figure(
    figsize=(7, 5)
)

ax = figure.add_subplot(111)

canvas = FigureCanvasTkAgg(
    figure,
    master=graph_frame
)

canvas.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=True
)


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()