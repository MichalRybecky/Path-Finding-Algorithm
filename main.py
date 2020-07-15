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
        self.open = False
        self.path = False

    def get_g_cost(self):
        # Getting node G cost
        if self.x == a_point_pos[0] and self.y == a_point_pos[1]:
            self.g = 0
        else:
            num_of_x_squares = (abs(a_point_pos[0] - self.x))
            num_of_y_squares = (abs(a_point_pos[1] - self.y))
            if num_of_y_squares == num_of_x_squares:
                self.g = num_of_x_squares / 50 * 70.71
            else:
                d = (num_of_x_squares ** 2) + (num_of_y_squares ** 2)
                self.g = math.sqrt(d)

    def get_h_cost(self):
        # Getting node H cost
        if self.x == b_point_pos[0] and self.y == b_point_pos [1]:
            self.h = 0
        else:
            num_of_x_squares = (abs(b_point_pos[0] - self.x))
            num_of_y_squares = (abs(b_point_pos[1] - self.y))
            if num_of_y_squares == num_of_x_squares:
                self.h = num_of_x_squares / 50 * 70.71
            else:
                d = (num_of_x_squares ** 2) + (num_of_y_squares ** 2)
                self.h = math.sqrt(d)

    def get_f_cost(self):
        # Getting node F cost
        self.f = self.g + self.h

    def draw_node(self, color):
        # Draw square and G, H and F cost in square
        c.create_rectangle(self.x, self.y, self.x + 50, self.y + 50, fill=color)
        c.create_text(self.x + 10, self.y + 10, text=int(self.g))
        c.create_text(self.x + 40, self.y + 10, text=int(self.h))
        c.create_text(self.x + 25, self.y + 30, text=int(self.f), font="arial 15 bold")

    def get_neighbours(self, x, y):
        # Adding node neighbours to list
        self.temp_neighbour_list.append([self.x - 50, self.y - 50])
        self.temp_neighbour_list.append([self.x - 50, self.y])
        self.temp_neighbour_list.append([self.x - 50, self.y + 50])

        self.temp_neighbour_list.append([self.x, self.y - 50])
        self.temp_neighbour_list.append([self.x, self.y + 50])

        self.temp_neighbour_list.append([self.x + 50, self.y - 50])
        self.temp_neighbour_list.append([self.x + 50, self.y])
        self.temp_neighbour_list.append([self.x + 50, self.y + 50])

        nodes_to_delete = []
        nodes_to_delete.clear()

        # Deleting nodes that are not on the grid or are walls
        for node in self.temp_neighbour_list:
            if node[0] < 50 or node[0] >= 750 or node[1] < 50 or node[1] >= 750 or node in walls_pos or node in closed_l:
                nodes_to_delete.append(node)
        for node in nodes_to_delete:
            self.temp_neighbour_list.remove(node)

        for node in self.temp_neighbour_list:
            self.neighbour_list.append(Node(node[0], node[1]))

        for node in self.neighbour_list:
            node.get_g_cost()
            node.get_h_cost()
            node.get_f_cost()
            node.draw_node("green")


    def get_neighbour_data(self, x, y):
        for node in self.neighbour_list:
            node.get_g_cost()
            node.get_h_cost()
            node.get_f_cost()


def lowest_f_cost_not_class():
        min_f_cost = min(open_l, key=attrgetter('f'))
        return min_f_cost


def main():
    # There is no A, B or both points on the screen
    if not a_point_pos or not b_point_pos:
        print("Missing point(s)")
    # Main loop
    else:
        a_node = Node(a_point_pos[0], a_point_pos[1])
        b_node = Node(b_point_pos[0], b_point_pos[1])
        a_node.open = True
        open_l.append(a_node)
        while True:
            current = lowest_f_cost_not_class()
            current.get_neighbours(current.x, current.y)
            current.get_neighbour_data(current.x, current.y)
            closed_l.append(current)
            open_l.remove(current)
            if current.x == b_node.x and current.y == b_node.y:
                break
                end()
            if current.x != a_node.x and current.y != a_node.y:
                current.draw_node("red")
            for neighbour in current.neighbour_list:
                if neighbour in closed_l:
                    continue
                if neighbour not in open_l:
                    neighbour.parent = current
                    open_l.append(neighbour)
        for node in closed_l:
            if node.parent == True:
                node.draw_node("blue")



            # open_l.append(current)
            # current.get_neighbours(current.x, current.y)
            # current.get_neighbour_data(current.x, current.y)
            # current = current.lowest_f_cost()
            # current = Node(current[0], current[1])




def mainboard():
    # Creating main board
    for i in range(14):
        for j in range(14):
            c.create_rectangle(j * 50 + 50, i * 50 + 50, j * 50 + 100, i * 50 + 100, fill="#E4E4E4")
    # Clearing list
    a_point_pos.clear()
    b_point_pos.clear()
    walls_pos.clear()
    # Start and Clear Buttons
    b_clear = Button(c, text="Clear", command=clear)
    b_clear.configure(width = 10, relief = FLAT)
    b_clear_window = c.create_window(300, 20, anchor=CENTER, window=b_clear)
    b_start = Button(c, text="Start", command=main)
    b_start.configure(width = 10, relief = FLAT)
    b_start_window = c.create_window(500, 20, anchor=CENTER, window=b_start)


def clear():
    c.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#E4E4E4")
    a_point_pos = []
    b_point_pos = []
    walls_pos = []
    open_l = []
    closed_l = []
    all_neighbours = []
    current = []
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
    # Creating A point (starting point)
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
    # Creating B point (ending point)
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
