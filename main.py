#!usr/bin/env python

import queue
import math
from tkinter import *
from operator import attrgetter

root = Tk()
root.title("Path finding algorithm")
root.geometry("800x800")
root.resizable(False,False)

WIDTH = 800
HEIGHT = 800

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
        self.wall = False
        self.neighbour_list = []
        self.parent = None

    def draw_node(self, color):
        # Draw square and G, H and F cost in square
        c.create_rectangle(self.x, self.y, self.x + 50, self.y + 50, fill=color)
        # G Cost - top left
        c.create_text(self.x + 10, self.y + 10, text=int(self.g))
        # H Cost - top right
        c.create_text(self.x + 40, self.y + 10, text=int(self.h))
        # F Cost - center
        c.create_text(self.x + 25, self.y + 30, text=int(self.f), font="arial 15 bold")

    def get_neighbours(self):
        # Adding node's neighbours to list
        for node in nodes:
            a = False
            if node.wall == True:
                continue
            elif node.x == self.x - 50 and node.y == self.y - 50:
                a = True
            elif node.x == self.x - 50 and node.y == self.y:
                a = True
            elif node.x == self.x - 50 and node.y == self.y + 50:
                a = True
            elif node.x == self.x and node.y == self.y - 50:
                a = True
            elif node.x == self.x and node.y == self.y + 50:
                a = True
            elif node.x == self.x + 50 and node.y == self.y - 50:
                a = True
            elif node.x == self.x + 50 and node.y == self.y:
                a = True
            elif node.x == self.x + 50 and node.y == self.y + 50:
                a = True

            if a == True:
                self.neighbour_list.append(node)

        for node in self.neighbour_list:
            node.g = heuristic(node, a_point_pos[0], a_point_pos[1])
            node.h = heuristic(node, b_point_pos[0], b_point_pos[1])
            node.f = node.g + node.h


def main():
    # There is no A, B or both points on the screen
    if not a_point_pos or not b_point_pos:
        print("Missing point(s)")
    else:
        a_node = Node(a_point_pos[0], a_point_pos[1])
        b_node = Node(b_point_pos[0], b_point_pos[1])
        open_l.append(a_node)
        # Main Loop
        while True:
            if len(open_l) == 0:
                no_possible_path()
                break
            current = min(open_l, key=attrgetter('f'))
            for node in open_l:
                if node.f == current.f and node.h < current.h:
                    current = node

            open_l.remove(current)
            closed_l.append(current)


            if current.x == b_node.x and current.y == b_node.y:
                for node in closed_l:
                    node.draw_node("blue")
                win()
                break

            current.get_neighbours()
            for neighbour in current.neighbour_list:
                if neighbour in closed_l or neighbour.wall == True:
                    continue

                if neighbour not in open_l:
                    neighbour.f = heuristic(neighbour, b_point_pos[0], b_point_pos[1])
                    neighbour.parent = current
                    if neighbour not in open_l:
                        open_l.append(neighbour)


            for node in current.neighbour_list:
                node.draw_node("green")
            current.draw_node("red")
            c.update()
            c.after(100)



# def lowest_f_cost():
#     # Finds and returns node (object) with lowest F cost in open_l
#     min_f_cost = min(open_l, key=attrgetter('f'))
#     return min_f_cost


def heuristic(current, end_x, end_y):
    # Calculates distance between two nodes
    dx = abs(end_x - current.x)
    dy = abs(end_y - current.y)
    minim = min(dx, dy)
    maxim = max(dx, dy)
    diagonal_steps = minim
    straight_steps = maxim - minim

    d = math.sqrt(2) * diagonal_steps + straight_steps
    return abs(d)


def mainboard():
    # Creating main board
    for i in range(14):
        for j in range(14):
            c.create_rectangle(j * 50 + 50, i * 50 + 50, j * 50 + 100, i * 50 + 100, fill="#E4E4E4")
            node = Node(j * 50 + 50, i * 50 + 50)
            nodes.append(node)
    # Start and Clear Buttons
    b_clear = Button(c, text="Clear", command=clear)
    b_clear.configure(width = 10, relief = FLAT)
    b_clear_window = c.create_window(300, 20, anchor=CENTER, window=b_clear)
    b_start = Button(c, text="Start", command=main)
    b_start.configure(width = 10, relief = FLAT)
    b_start_window = c.create_window(500, 20, anchor=CENTER, window=b_start)


def clear():
    c.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#E4E4E4")
    a_node = None
    b_node = None
    a_point_pos.clear()
    b_point_pos.clear()
    walls_pos.clear()
    open_l.clear()
    closed_l.clear()
    all_neighbours = []
    current = None
    mainboard()


def no_possible_path():
    print("There is no path!")


def win():
    print("done")
    a_x, a_y = a_point_pos[0], a_point_pos[1]
    b_x, b_y = b_point_pos[0], b_point_pos[1]
    c.create_rectangle(a_x, a_y, a_x + 50, a_y + 50, fill = "blue")
    c.create_text(a_x + 25, a_y + 25, text="A", font="arial 20 bold")

    c.create_rectangle(b_x, b_y, b_x + 50, b_y + 50, fill = "blue")
    c.create_text(b_x + 25, b_y + 25, text="B", font="arial 20 bold")


def square_clicked(x, y):
    # Returns which square was clicked
    x_minus = x % 50
    x -= x_minus
    y_minus = y % 50
    y -= y_minus
    return x, y


def square_erease(x, y):
    # Ereases square
    c.create_rectangle(x, y, x + 50, y + 50, fill="#E4E4E4")


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


def create_a(event):
    # Creating A point (starting node)
    x, y = square_clicked(event.x, event.y)
    if x < 50 or x >= 750 or y < 50 or y >= 750:
        pass
    else:
        if a_point_pos:
            square_erease(a_point_pos[0], a_point_pos[1])
            a_point_pos.clear()
        square_overlap(x, y, "a_overlap_b")
        square_overlap(x, y, "overlap_wall")
        c.create_rectangle(x, y, x + 50, y + 50, fill = "blue")
        c.create_text(x + 25, y + 25, text="A", font="arial 20 bold")
        a_point_pos.append(x)
        a_point_pos.append(y)


def create_b(event):
    # Creating B point (ending node)
    x, y = square_clicked(event.x, event.y)
    if x < 50 or x >= 750 or y < 50 or y >= 750:
        pass
    else:
        if b_point_pos:
            square_erease(b_point_pos[0], b_point_pos[1])
            b_point_pos.clear()
        square_overlap(x, y, "b_overlap_a")
        square_overlap(x, y, "overlap_wall")
        c.create_rectangle(x, y, x + 50, y + 50, fill = "blue")
        c.create_text(x + 25, y + 25, text="B", font="arial 20 bold")
        b_point_pos.append(x)
        b_point_pos.append(y)

# Lists storing point and walls positions
a_point_pos = []
b_point_pos = []
walls_pos = []
nodes = []
open_l = []
closed_l = []
all_neighbours = []
current = []


mainboard()

# Mouse buttons binding
c.bind("<1>", create_a)
c.bind("<B2-Motion>", create_wall)
c.bind("<3>", create_b)


root.mainloop()
c.mainloop()
