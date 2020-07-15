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
        self.temp_neighbour_list = []
        self.neighbour_list = []
        self.parent = None
        self.closed = False

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
        # Left column
        self.temp_neighbour_list.append([self.x - 50, self.y - 50])
        self.temp_neighbour_list.append([self.x - 50, self.y])
        self.temp_neighbour_list.append([self.x - 50, self.y + 50])

        # Mid column
        self.temp_neighbour_list.append([self.x, self.y - 50])
        self.temp_neighbour_list.append([self.x, self.y + 50])

        # Right column
        self.temp_neighbour_list.append([self.x + 50, self.y - 50])
        self.temp_neighbour_list.append([self.x + 50, self.y])
        self.temp_neighbour_list.append([self.x + 50, self.y + 50])

        nodes_to_delete = []
        nodes_to_delete.clear()

        # Deleting nodes that are not on the grid or are walls
        for node in self.temp_neighbour_list:
            if node[0] < 50 or node[0] >= 750 or node[1] < 50 or node[1] >= 750 or node in walls_pos:
                nodes_to_delete.append(node)

        for node in nodes_to_delete:
            self.temp_neighbour_list.remove(node)

        for node in self.temp_neighbour_list:
            self.neighbour_list.append(Node(node[0], node[1]))

        for node in self.neighbour_list:
            node.g = heuristic(node, a_point_pos[0], a_point_pos[1])
            node.h = heuristic(node, b_point_pos[0], b_point_pos[1])
            node.f = node.g + node.h


def main():
    # There is no A, B or both points on the screen
    if not a_point_pos or not b_point_pos:
        print("Missing point(s)")
    # Main loop
    else:
        current = Node(a_point_pos[0], a_point_pos[1])
        b_node = Node(b_point_pos[0], b_point_pos[1])
        open_l.append(current)
        while True:
            current = lowest_f_cost()
            open_l.remove(current)
            closed_l.append(current)
            current.draw_node("red")

            if current.x == b_node.x and current.y == b_node.y:
                win()
                break

            current.get_neighbours()
            for neighbour in current.neighbour_list:
                if neighbour in closed_l:
                    continue

                if neighbour not in open_l:
                    neighbour.parent = current
                    open_l.append(neighbour)



            for node in current.neighbour_list:
                if node not in open_l or node not in closed_l:
                    node.draw_node("green")


            # open_l.append(current)
            # current.get_neighbours(current.x, current.y)
            # current = current.lowest_f_cost()
            # current = Node(current[0], current[1])


def lowest_f_cost():
    # Finds and returns node (object) with lowest F cost in open_l
    min_f_cost = min(open_l, key=attrgetter('f'))
    return min_f_cost


def heuristic(current, end_x, end_y):
    # Calculates distance between two nodes
    dx = abs(end_x - current.x)
    dy = abs(end_y - current.y)
    minim = min(dx, dy)
    maxim = max(dx, dy)
    diagonal_steps = minim
    straight_steps = maxim - minim

    d = math.sqrt(2) * diagonal_steps + straight_steps
    return d


def mainboard():
    # Creating main board
    for i in range(14):
        for j in range(14):
            c.create_rectangle(j * 50 + 50, i * 50 + 50, j * 50 + 100, i * 50 + 100, fill="#E4E4E4")
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


def win():
    print("done")


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
    elif type == "overlap_wall":
        if walls_pos:
            if [x, y] in walls_pos:
                walls_pos.remove([x, y])


def create_wall(event):
    # Creating walls
    x, y = square_clicked(event.x, event.y)
    if x < 50 or x >= 750 or y < 50 or y >= 750:
        pass
    elif [x, y] in walls_pos:
        square_erease(x, y)
        walls_pos.remove([x, y])
    else:
        c.create_rectangle(x, y, x + 50, y + 50, fill = "grey")
        walls_pos.append([x, y])


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
open_l = []
closed_l = []
all_neighbours = []
current = []


mainboard()

# Mouse buttons binding
c.bind("<1>", create_a)
c.bind("<2>", create_wall)
c.bind("<3>", create_b)


root.mainloop()
c.mainloop()
