#!usr/bin/env python

from time import time
from math import sqrt
from tkinter import *
from operator import attrgetter

# WIDTH is both width and height
WIDTH = 800
NODE_SIZE = 25

root = Tk()
root.title("Path finding algorithm")
root.geometry(f"{WIDTH}x{WIDTH}")
root.resizable(False, False)

c = Canvas(root, width=WIDTH, height=WIDTH, background="#E4E4E4")
c.pack()

"""
IMPORTANT VALUES:
G cost = distance from A (top left)
H cost = distance from B (top right)
F cost = overall distance, G cost + H cost (center)
Square is 50x50, diagonal is 70,71
"""


class Node:
    """
    Node object is every node (square) on the screen.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.is_a = False
        self.is_b = False
        self.wall = False
        self.parent = None
        self.neighbour_list = []

    def draw_node(self, color):
        """
        Draws node and G, H and F cost in square
        """
        self.f_cost = self.g_cost + self.h_cost
        c.create_rectangle(
            self.x, self.y, self.x + NODE_SIZE, self.y + NODE_SIZE, fill=color
        )
        if not draw_data.get():
            c.create_text(
                self.x + NODE_SIZE / 4,
                self.y + NODE_SIZE / 5,
                text=int(self.g_cost),
                font=f"arial {int(NODE_SIZE / 5)}",
            )
            c.create_text(
                self.x + NODE_SIZE / 4 * 3,
                self.y + NODE_SIZE / 5,
                text=int(self.h_cost),
                font=f"arial {int(NODE_SIZE / 5)}",
            )
            c.create_text(
                self.x + NODE_SIZE / 2,
                self.y + NODE_SIZE / 5 * 3,
                text=int(self.f_cost),
                font=f"arial {int(NODE_SIZE / 10 * 3)} bold",
            )

    def get_neighbours(self):
        """
        Adds node's neighbours to his list
        """
        x = -NODE_SIZE
        for _ in range(3):
            y = -NODE_SIZE
            for _ in range(3):
                if x == 0 and y == 0:
                    y += NODE_SIZE
                    continue
                else:
                    check_x = self.x + x
                    check_y = self.y + y

                    for node in nodes:
                        if node.x == check_x and node.y == check_y:
                            self.neighbour_list.append(node)
                    y += NODE_SIZE
            x += NODE_SIZE


class RuntimeError(Exception):
    """
    Exception raised when a specific error code is needed
    """

    def __init__(self, message, code):
        super().__init__(f"Error code {code}: {message}")
        self.code = code


def algorithm():
    """
    Main algorithm of program, this is where the magic happens
    """
    start = time()
    # There is no A, B or both points on the screen
    if not a_point_pos or not b_point_pos:
        print("Missing point(s)")
    else:
        for node in nodes:
            if node.is_a:
                open_l.append(node)
                break
        # Algorithm Loop
        while True:
            # No more possible nodes to explore, meaning path is not existing
            if len(open_l) == 0:
                print("There is no path!")
                c.create_text(
                    WIDTH / 2,
                    WIDTH - 25,
                    text="There is no path!",
                    font="arial 20",
                    fill="red",
                )
                break
            # Selects the node with the lowest F and H cost as current
            current = min(open_l, key=attrgetter("f_cost"))
            for node in open_l:
                if node.f_cost == current.f_cost and node.h_cost < current.h_cost:
                    current = node

            open_l.remove(current)
            closed_l.append(current)

            # Current node is on B node, meaning the path has been explored
            if current.x == b_point_pos[0] and current.y == b_point_pos[1]:
                retrace()
                break

            # Getting neighbours and their data
            current.get_neighbours()
            for neighbour in current.neighbour_list:
                if neighbour in closed_l or neighbour.wall:
                    continue

                new_movement_cost_to_neighbour = current.g_cost + heuristic(
                    current, neighbour
                )
                if (
                    new_movement_cost_to_neighbour < neighbour.g_cost
                    or neighbour not in open_l
                ):
                    neighbour.g_cost = new_movement_cost_to_neighbour
                    for node in nodes:
                        if node.is_b:
                            neighbour.h_cost = heuristic(neighbour, node)
                            break
                    neighbour.parent = current
                    if neighbour not in open_l:
                        open_l.append(neighbour)

            # Drawing only neighbourous nodes for faster execution
            for node in open_l:
                if node in current.neighbour_list:
                    node.draw_node("green")

            for node in closed_l:
                if node in current.neighbour_list:
                    node.draw_node("red")
            draw("A")
            draw("B")
            c.update()
    runtime = float(time() - start)
    print(f"Runtime of main algorithm: {round(runtime, 5)}")


def retrace():
    """
    Retraces and redraws the shortest path after the path has been found
    """
    path = []
    a_node = None
    for node in nodes:
        if node.x == b_point_pos[0] and node.y == b_point_pos[1]:
            current = node
            break

    for node in nodes:
        if node.is_a:
            a_node = node
            break

    while current != a_node:
        path.append(current)
        current = current.parent

    for node in path:
        node.draw_node("blue")
        draw("B")
        c.update()
        c.after(50)
    print("Path found!")


def heuristic(current, target):
    """
    Calculates total distance between two nodes
    """
    dist_x = abs(target.x - current.x)
    dist_y = abs(target.y - current.y)
    minimum = min(dist_x, dist_y)
    maximum = max(dist_x, dist_y)
    diagonal_steps = minimum
    straight_steps = maximum - minimum

    dist = sqrt(2) * diagonal_steps + straight_steps
    return abs(dist)


def mainboard():
    """
    Grid and adding nodes to objects
    """
    c.create_rectangle(0, 0, WIDTH, WIDTH, fill="#E4E4E4")
    nodes.clear()
    i = 50
    j = 50
    while i < WIDTH - 50:
        while j < WIDTH - 50:
            c.create_rectangle(i, j, i + NODE_SIZE, j + NODE_SIZE, fill="#E4E4E4")
            node = Node(i, j)
            nodes.append(node)
            j += NODE_SIZE
        j = 50
        i += NODE_SIZE

    # Start and Clear Buttons
    b_start = Button(c, text="Start", command=algorithm)
    b_start.configure(width=10, relief=FLAT)
    c.create_window(WIDTH / 5, 20, anchor=CENTER, window=b_start)
    b_clear = Button(c, text="Clear", command=clear)
    b_clear.configure(width=10, relief=FLAT)
    c.create_window(WIDTH / 5 * 2, 20, anchor=CENTER, window=b_clear)
    b_about = Button(c, text="About", command=about)
    b_about.configure(width=10, relief=FLAT)
    c.create_window(WIDTH / 5 * 3, 20, anchor=CENTER, window=b_about)
    # Check for drawing data
    check_data = Checkbutton(c, text="Draw data", var=draw_data)
    c.create_window(WIDTH / 5 * 4, 20, anchor=CENTER, window=check_data)


def about():
    """
    Opens new window with text about application
    """

    def create_text_about(text, y, size=15):
        c_about.create_text(20, y, text=text, anchor=W, font=f"System {size} normal")

    WIDTH_A = WIDTH
    HEIGHT_A = int(WIDTH / 2)
    about = Tk()
    about.title("Path finding algorithm")
    about.geometry(f"{WIDTH_A}x{HEIGHT_A}")
    about.resizable(False, False)
    c_about = Canvas(about, width=WIDTH_A, height=HEIGHT_A, background="#E4E4E4")
    c_about.pack()

    # Labels
    texts = [
        ["How to use this program:", 20, 20],
        ["Click right mouse button to draw Start/A and End/B point on the grid.", 50],
        ["Drag left mouse button to draw Walls.", 80],
        ["Click on Start button to begin the algorithm.", 110],
        ["Use Clear button to clear the grid and repeat.", 140],
    ]
    for text in texts:
        create_text_about(*text)

    about.mainloop()
    c_about.mainloop()


def clear():
    a_point_pos.clear()
    b_point_pos.clear()
    open_l.clear()
    closed_l.clear()
    mainboard()


def square_clicked(x, y):
    """
    Returns x and y of clicked square
    """
    x -= x % NODE_SIZE
    y -= y % NODE_SIZE
    return x, y


def square_erease(x, y):
    """
    Ereases square leaving blanc canvas
    """
    c.create_rectangle(x, y, x + NODE_SIZE, y + NODE_SIZE, fill="#E4E4E4")


def square_overlap(x, y):
    """
    Overlap of nodes handling
    """
    for node in nodes:
        if node.x == x and node.y == y:
            if not node.wall or node.is_a or node.is_b:
                return True


def create_wall(event):
    """
    Creates walls upon mouse button 1 press and drag
    """
    x, y = square_clicked(event.x, event.y)
    for node in nodes:
        if node.x == x and node.y == y and not node.wall:
            node.wall = True
            c.create_rectangle(x, y, x + NODE_SIZE, y + NODE_SIZE, fill="grey")
            break


def create_node(event):
    """
    Creates A or B node
    """
    x, y = square_clicked(event.x, event.y)
    if square_overlap(x, y):
        if not a_point_pos:
            for node in nodes:
                if node.x == x and node.y == y:
                    node.is_a = True
                    a_node = node
                    a_point_pos.extend([x, y])
                    draw("A")
                    break
        else:
            for node in nodes:
                if node.x == x and node.y == y:
                    node.is_b = True
                    b_node = node
                    b_point_pos.extend([x, y])
                    draw("B")
                    break


def draw(type):
    """
    Draws either A or B node, depending on the 'type' value (Can be 'A' or 'B')
    """
    if type == "A":
        c.create_rectangle(
            a_point_pos[0],
            a_point_pos[1],
            a_point_pos[0] + NODE_SIZE,
            a_point_pos[1] + NODE_SIZE,
            fill="blue",
        )
        c.create_text(
            a_point_pos[0] + NODE_SIZE / 2,
            a_point_pos[1] + NODE_SIZE / 2,
            text="A",
            font="arial 20 bold",
        )
    elif type == "B":
        c.create_rectangle(
            b_point_pos[0],
            b_point_pos[1],
            b_point_pos[0] + NODE_SIZE,
            b_point_pos[1] + NODE_SIZE,
            fill="blue",
        )
        c.create_text(
            b_point_pos[0] + NODE_SIZE / 2,
            b_point_pos[1] + NODE_SIZE / 2,
            text="B",
            font="arial 20 bold",
        )
    else:
        raise RuntimeError("Invalid node type", 100)


if __name__ == "__main__":
    # Lists storing point and walls positions
    draw_data = StringVar()
    a_point_pos = []
    b_point_pos = []
    nodes = []
    open_l = []
    closed_l = []

    mainboard()

    # Mouse buttons binding
    c.bind("<B1-Motion>", create_wall)
    c.bind("<3>", create_node)

    root.mainloop()
    c.mainloop()
