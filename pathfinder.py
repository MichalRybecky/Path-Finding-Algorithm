#!usr/bin/env python

from math import sqrt
from tkinter import *
from operator import attrgetter

# WIDTH is both width and height
WIDTH = 800
NODE_SIZE = 25

root = Tk()
root.title("Path finding algorithm")
root.geometry(f"{WIDTH}x{WIDTH}")
root.resizable(False,False)

c = Canvas(root, width=WIDTH, height=WIDTH, background="#E4E4E4")
c.pack()

'''
G cost = distance from A (top left)
H cost = distance from B (top right)
F cost = overall distance, G cost + H cost (center)sublime text 3 programming settings
Square is 50x50, diagonal is 70,71
'''

class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.is_a = False
        self.is_b = False
        self.wall = False
        self.neighbour_list = []
        self.parent = None

    def draw_node(self, color):
        # Draws node and G, H and F cost in square
        self.f = self.g + self.h
        c.create_rectangle(self.x, self.y, self.x + NODE_SIZE, self.y + NODE_SIZE, fill=color)
        if not draw_data.get():
            c.create_text(self.x + NODE_SIZE / 4, self.y + NODE_SIZE / 5, text=int(self.g), font=f"arial {int(NODE_SIZE / 5)}")
            c.create_text(self.x + NODE_SIZE / 4 * 3, self.y + NODE_SIZE / 5, text=int(self.h), font=f"arial {int(NODE_SIZE / 5)}")
            c.create_text(self.x + NODE_SIZE / 2, self.y + NODE_SIZE / 5 * 3, text=int(self.f), font=f"arial {int(NODE_SIZE / 10 * 3)} bold")

    def get_neighbours(self):
        # Adds node's neighbours to his list
        x = -NODE_SIZE
        for i in range(3):
            y = -NODE_SIZE
            for j in range(3):
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


def algorithm():
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
                break
            # Selects the node with the lowest F and H cost as current
            current = min(open_l, key=attrgetter('f'))
            for node in open_l:
                if node.f == current.f and node.h < current.h:
                    current = node
                    break

            open_l.remove(current)
            closed_l.append(current)

            # Current node is on B node, meaning the path has been explored
            if current.x == b_point_pos[0] and current.y == b_point_pos[1]:
                retrace()
                break

            # Getting neighbours and their data
            current.get_neighbours()
            for neighbour in current.neighbour_list:
                if neighbour in closed_l or neighbour.wall == True:
                    continue

                new_movement_cost_to_neighbour = current.g + heuristic(current, neighbour)
                if new_movement_cost_to_neighbour < neighbour.g or neighbour not in open_l:
                    neighbour.g = new_movement_cost_to_neighbour
                    for node in nodes:
                        if node.is_b:
                            neighbour.h = heuristic(neighbour, node)
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



def retrace():
    # Retraces and redraws the shortest path after the path has been found
    path = []
    dist = []
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


def draw(type):
    # Draws either A or B node, depending on the input
    if type == "A":
        c.create_rectangle(a_point_pos[0], a_point_pos[1], a_point_pos[0] + NODE_SIZE, a_point_pos[1] + NODE_SIZE, fill = "blue")
        c.create_text(a_point_pos[0] + NODE_SIZE / 2, a_point_pos[1] + NODE_SIZE / 2, text="A", font="arial 20 bold")
    else:
        c.create_rectangle(b_point_pos[0], b_point_pos[1], b_point_pos[0] + NODE_SIZE, b_point_pos[1] + NODE_SIZE, fill = "blue")
        c.create_text(b_point_pos[0] + NODE_SIZE / 2, b_point_pos[1] + NODE_SIZE / 2, text="B", font="arial 20 bold")


def heuristic(current, target):
    # Calculates distance between two nodes
    dx = abs(target.x - current.x)
    dy = abs(target.y - current.y)
    minim = min(dx, dy)
    maxim = max(dx, dy)
    diagonal_steps = minim
    straight_steps = maxim - minim

    d = sqrt(2) * diagonal_steps + straight_steps
    return abs(d)


def mainboard():
    # Grid and adding nodes to objects
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
    b_start.configure(width = 10, relief = FLAT)
    b_start_window = c.create_window(WIDTH / 5, 20, anchor=CENTER, window=b_start)
    b_clear = Button(c, text="Clear", command=clear)
    b_clear.configure(width = 10, relief = FLAT)
    b_clear_window = c.create_window(WIDTH / 5 * 2, 20, anchor=CENTER, window=b_clear)
    b_about = Button(c, text="About", command=about)
    b_about.configure(width = 10, relief = FLAT)
    b_about_window = c.create_window(WIDTH / 5 * 3, 20, anchor=CENTER, window=b_about)
    # Check for drawing data
    check_data = Checkbutton(c, text="Draw data", var=draw_data)
    check_data_window = c.create_window(WIDTH / 5 * 4, 20, anchor=CENTER, window=check_data)


def about():
    WIDTH_A = WIDTH
    HEIGHT_A = int(WIDTH / 2)
    about = Tk()
    about.title("Path finding algorithm")
    about.geometry(f"{WIDTH_A}x{HEIGHT_A}")
    about.resizable(False,False)
    c_about = Canvas(about, width=WIDTH_A, height=HEIGHT_A, background="#E4E4E4")
    c_about.pack()

    # Labels
    text = "How to use this program:"
    c_about.create_text(20, 20, text=text, anchor=W, font="System 20 normal")
    text = "Click right mouse button to draw Start/A and End/B point on the grid."
    c_about.create_text(20, 50, text=text, anchor=W, font="System 15 normal")
    text = "Drag left mouse button to draw Walls."
    c_about.create_text(20, 80, text=text, anchor=W, font="System 15 normal")
    text = "Click on Start button to begin the algorithm."
    c_about.create_text(20, 110, text=text, anchor=W, font="System 15 normal")
    text = "Use Clear button to clear the grid and repeat."
    c_about.create_text(20, 140, text=text, anchor=W, font="System 15 normal")

    about.mainloop()
    c_about.mainloop()



def clear():
    a_point_pos.clear()
    b_point_pos.clear()
    open_l.clear()
    closed_l.clear()
    mainboard()


def square_clicked(x, y):
    # Returns x and y of clicked square
    x -= x % NODE_SIZE
    y -= y % NODE_SIZE
    return x, y


def square_erease(x, y):
    # Ereases square
    c.create_rectangle(x, y, x + NODE_SIZE, y + NODE_SIZE, fill="#E4E4E4")


def square_overlap(x, y):
    # Overlap of nodes handling
    for node in nodes:
        if node.x == x and node.y == y:
            if node.wall == False or node.is_a or node.is_b:
                return True
                break


def create_wall(event):
    # Creating walls
    x, y = square_clicked(event.x, event.y)
    for node in nodes:
        if node.x == x and node.y == y:
            node.wall = True
            c.create_rectangle(x, y, x + NODE_SIZE, y + NODE_SIZE, fill = "grey")
            break


def create_node(event):
    # Creates A or B node
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
