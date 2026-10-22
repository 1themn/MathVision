
import tkinter as tk
from viewport import Viewport
import math
from grid import GridRenderer
from graph import parse_equation
from equation_renderer import EquationRenderer
import time

WIDTH = 1500
HEIGHT = 1000
SCALE = 50

viewport = Viewport(WIDTH, HEIGHT, SCALE)



root = tk.Tk()
root.title("Infinite Grid")
root.geometry(f"{WIDTH}x{HEIGHT}")

sidebar = tk.Frame(
    root,
    width=280,
    bg="#1e293b"
)

sidebar.pack(
    side=tk.LEFT,
    fill=tk.Y
)

sidebar.pack_propagate(False)

graph_frame = tk.Frame(root)

graph_frame.pack(
    side=tk.RIGHT,
    fill=tk.BOTH,
    expand=True
)

canvas = tk.Canvas(
    graph_frame,
    bg="#101827",
    highlightthickness=0
)

canvas.pack(
    fill=tk.BOTH,
    expand=True
)



origin_x = WIDTH / 2
origin_y = HEIGHT / 2

renderer = GridRenderer(canvas, viewport)

equation_renderer = EquationRenderer(
    canvas,
    viewport
)

equations = []


def draw_grid():
    renderer.draw()

    for item in equations:
        if not item["visible"].get():
            continue

        equation = item["equation"]
        color = item["color"]

        if equation.equation_type == "explicit":
            equation_renderer.draw_explicit(
                equation,
                color
            )
        else:
            equation_renderer.draw_implicit(
                equation,
                color
            )


equation_label = tk.Label(
    sidebar,
    text="Equations",
    bg="#1e293b",
    fg="white",
    font=("Arial", 14, "bold")
)

equation_label.pack(
    anchor="w",
    padx=10,
    pady=(15, 10)
)

equation_entry = tk.Entry(
    sidebar,
    font=("Arial", 12)
)

equation_entry.pack(
    fill=tk.X,
    padx=10,
    pady=5
)

add_button = tk.Button(
    sidebar,
    text="Add Equation",
    command=lambda: add_equation()
)

add_button.pack(
    fill=tk.X,
    padx=10,
    pady=5
)
error_label = tk.Label(
    sidebar,
    text="",
    fg="#f87171",
    bg="#1e293b",
    wraplength=250
)

error_label.pack(fill=tk.X, padx=10)
equation_entry.bind(
    "<Return>",
    lambda event: add_equation()
)
equation_frame = tk.Frame(
    sidebar,
    bg="#1e293b"
)

equation_frame.pack(
    fill=tk.X,
    padx=10,
    pady=10
)
COLORS = [
    "#60a5fa",
    "#f472b6",
    "#4ade80",
    "#facc15",
    "#c084fc"
]

def add_equation():
    equation_text = equation_entry.get().strip()

    if not equation_text:
        return

    try:
        parsed_equation = parse_equation(equation_text)

        

    except (ValueError, SyntaxError, TypeError):
        error_label.config(text="Invalid equation.")
        return

    error_label.config(text="")

    equation_data = {
        "equation": parsed_equation,
        "text": equation_text,
        "color": COLORS[len(equations) % len(COLORS)],
        "visible": tk.BooleanVar(value=True)
    }

    equations.append(equation_data)

    create_equation_row(equation_data)

    equation_entry.delete(0, tk.END)

    draw_grid()

def remove_equation(equation_data, row):
    equations.remove(equation_data)

    row.destroy()

    draw_grid()

def create_equation_row(equation_data):
    row = tk.Frame(
        equation_frame,
        bg="#1e293b"
    )

    row.pack(fill=tk.X, pady=4)

    checkbox = tk.Checkbutton(
        row,
        variable=equation_data["visible"],
        command=draw_grid,
        bg="#1e293b",
        activebackground="#1e293b"
    )

    checkbox.pack(side=tk.LEFT)

    label = tk.Label(
        row,
        text=equation_data["text"],
        fg=equation_data["color"],
        bg="#1e293b",
        anchor="w"
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




def handle_resize(event):
    viewport.width = event.width
    viewport.height = event.height

    draw_grid()


def format_coordinate(value):
    if abs(value) < 1e-10:
        return "0"

    return f"{value:.10g}"


draw_grid()



last_mouse_x = 0
last_mouse_y = 0


def start_pan(event):
    global last_mouse_x, last_mouse_y

    last_mouse_x = event.x
    last_mouse_y = event.y


def drag_pan(event):
    global last_mouse_x, last_mouse_y

    dx = event.x - last_mouse_x
    dy = event.y - last_mouse_y

    viewport.pan(dx, dy)

    last_mouse_x = event.x
    last_mouse_y = event.y

    draw_grid()






def normalize_delta(delta):
    value = delta & 0xFFFF

    if value >= 32768:
        value -= 65536

    return value


def handle_touchpad_zoom(event):
    delta = normalize_delta(event.delta)

    if delta == 0:
        return

    # Limit unusually large movements
    delta = max(-20, min(20, delta))

    # Smooth proportional zoom
    factor = 1.003 ** delta

    viewport.zoom(event.x, event.y, factor)
    draw_grid()







def handle_mouse_zoom(event):
    if getattr(event, "num", None) == 4:
        factor = 1.1

    elif getattr(event, "num", None) == 5:
        factor = 1 / 1.1

    elif getattr(event, "delta", 0) > 0:
        factor = 1.1

    elif getattr(event, "delta", 0) < 0:
        factor = 1 / 1.1

    else:
        return

    viewport.zoom(event.x, event.y, factor)
    draw_grid()






canvas.bind("<ButtonPress-1>", start_pan)
canvas.bind("<B1-Motion>", drag_pan)

canvas.bind("<TouchpadScroll>", handle_touchpad_zoom)
canvas.bind("<MouseWheel>", handle_mouse_zoom)

# Linux mouse wheel support
canvas.bind("<Button-4>", handle_mouse_zoom)
canvas.bind("<Button-5>", handle_mouse_zoom)

canvas.bind("<Configure>", handle_resize)
root.mainloop()
