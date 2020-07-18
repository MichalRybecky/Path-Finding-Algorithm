#!usr/bin/env python

from math import sqrt
from tkinter import *
from operator import attrgetter

WIDTH = 800
HEIGHT = 800

root = Tk()
root.title("Path finding algorithm")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False,False)

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#E4E4E4")
c.pack()

'''
G cost = distance from A (top left)
H cost = distance from B (top right)
F cost = overall distance, G cost + H cost (center)
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
        c.create_rectangle(self.x, self.y, self.x + 50, self.y + 50, fill=color)
        if not draw_data.get():
            c.create_text(self.x + 10, self.y + 10, text=int(self.g))
            c.create_text(self.x + 40, self.y + 10, text=int(self.h))
            c.create_text(self.x + 25, self.y + 30, text=int(self.f), font="arial 15 bold")

    def get_neighbours(self):
        # Adds node's neighbours to his list
        x = -50
        for i in range(3):
            y = -50
            for j in range(3):
                if x == 0 and y == 0:
                    y += 50
                    continue
                else:
                    check_x = self.x + x
                    check_y = self.y + y

                    for node in nodes:
                        if node.x == check_x and node.y == check_y:
                            self.neighbour_list.append(node)
                    y += 50
            x += 50


def algorithm():
    # There is no A, B or both points on the screen
    if not a_point_pos or not b_point_pos:
        print("Missing point(s)")
    else:
        for node in nodes:
            if node.is_a:
                open_l.append(node)
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
                    neighbour.parent = current
                    if neighbour not in open_l:
                        open_l.append(neighbour)


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
    path = []
    dist = []
    a_node = None
    for node in nodes:
        if node.x == b_point_pos[0] and node.y == b_point_pos[1]:
            current = node
    for node in nodes:
        if node.is_a:
            a_node = node

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
        c.create_rectangle(a_point_pos[0], a_point_pos[1], a_point_pos[0] + 50, a_point_pos[1] + 50, fill = "blue")
        c.create_text(a_point_pos[0] + 25, a_point_pos[1] + 25, text="A", font="arial 20 bold")
    else:
        c.create_rectangle(b_point_pos[0], b_point_pos[1], b_point_pos[0] + 50, b_point_pos[1] + 50, fill = "blue")
        c.create_text(b_point_pos[0] + 25, b_point_pos[1] + 25, text="B", font="arial 20 bold")


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
    # Creating main board
    nodes.clear()
    for i in range(14):
        for j in range(14):
            c.create_rectangle(j * 50 + 50, i * 50 + 50, j * 50 + 100, i * 50 + 100, fill="#E4E4E4")
            node = Node(j * 50 + 50, i * 50 + 50)
            nodes.append(node)
    # Start and Clear Buttons
    b_clear = Button(c, text="Clear", command=clear)
    b_clear.configure(width = 10, relief = FLAT)
    b_clear_window = c.create_window(300, 20, anchor=CENTER, window=b_clear)
    b_start = Button(c, text="Start", command=algorithm)
    b_start.configure(width = 10, relief = FLAT)
    b_start_window = c.create_window(500, 20, anchor=CENTER, window=b_start)
    # Check for drawing data
    check_data = Checkbutton(c, text="Draw data", var=draw_data)
    check_data_window = c.create_window(WIDTH - 50, HEIGHT - 30, anchor=E, window=check_data)
    # Labels
    text = "Click right mouse button to draw Start and End point on the grid."
    c.create_text(20, HEIGHT - 35, text=text, anchor=W, font="System 15 normal")
    text = "Click and drag left mouse button to draw Walls."
    c.create_text(20, HEIGHT - 15, text=text, anchor=W, font="System 15 normal")

def clear():
    a_point_pos.clear()
    b_point_pos.clear()
    open_l.clear()
    closed_l.clear()
    current = None
    mainboard()


def square_clicked(x, y):
    # Returns x and y of clicked square
    x_minus = x % 50
    x -= x_minus
    y_minus = y % 50
    y -= y_minus
    return x, y


def square_erease(x, y):
    # Ereases square
    c.create_rectangle(x, y, x + 50, y + 50, fill="#E4E4E4")


# This function is no longer working, need to fix it
def square_overlap(x, y, type):
    # Overlap handling
    if type == "a_overlap_b":
        if b_point_pos:
            if x == b_point_pos[0] and y == b_point_pos[1]:
                b_point_pos.clear()
    elif type == "b_overlap_a":
        if a_point_pos:
            if x == a_point_pos[0] and y == a_point_pos[1]:
                a_point_pos.clear()


def create_wall(event):
    # Creating walls
    x, y = square_clicked(event.x, event.y)
    for node in nodes:
        if node.x == x and node.y == y:
            node.wall = True
            c.create_rectangle(x, y, x + 50, y + 50, fill = "grey")


def create_node(event):
    # Creates A or B node
    x, y = square_clicked(event.x, event.y)
    if not a_point_pos:
        square_overlap(x, y, "a_overlap_b")
        square_overlap(x, y, "overlap_wall")
        for node in nodes:
            if node.x == x and node.y == y:
                node.is_a = True
                a_node = node
                a_point_pos.extend([x, y])
                draw("A")
    else:
        square_overlap(x, y, "b_overlap_a")
        square_overlap(x, y, "overlap_wall")
        for node in nodes:
            if node.x == x and node.y == y:
                node.is_b = True
                b_node = node
                b_point_pos.extend([x, y])
                draw("B")

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
