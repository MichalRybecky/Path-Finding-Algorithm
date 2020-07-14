import queue
from tkinter import *

root = Tk()
root.title("Path finding algorithm")
root.geometry("800x800")
root.resizable(False,False)

c = Canvas(root, width=800, height=800, background="#E4E4E4")
c.pack()


'''
G cost = distance from A (top left)
H cost = distance from B (top right)
F cost = overall distance, G cost + H cost (center)

Square is 50x50, diagonal is 70,71
'''


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.neighbour_list = []

    def get_g_cost(self, x, y):
        if self.x == a_point_pos[0] and self.y == a_point_pos [1]:
            self.g = 0
        else:
            g_cost = []
            g_cost.clear()
            g_cost.append(abs(a_point_pos[0] - self.x))
            g_cost.append(abs(a_point_pos[1] - self.y))

            num_of_x_squares = int(g_cost[0])
            num_of_y_squares = int(g_cost[1])

            self.g = abs((num_of_x_squares - num_of_y_squares) + (((num_of_y_squares - 50) / 50) * 70.71))
        print(f"G cost: {self.g}")

    def get_h_cost(self, x, y):
        if self.x == b_point_pos[0] and self.y == b_point_pos [1]:
            self.h = 0
        else:
            h_cost = []
            h_cost.clear()
            h_cost.append(abs(b_point_pos[0] - self.x))
            h_cost.append(abs(b_point_pos[1] - self.y))

            num_of_x_squares = int(h_cost[0])
            num_of_y_squares = int(h_cost[1])

            self.h = abs((num_of_x_squares - num_of_y_squares) + (((num_of_y_squares - 50) / 50) * 70.71))
        print(f"H cost: {self.h}")

    def get_f_cost(self, x, y):
        self.f = self.g + self.h
        print(f"F cost: {self.f}")

    def draw_node(self, x, y, g, h, f):
        # Draw square and G, H and F cost in square
        c.create_rectangle(self.x, self.y, self.x + 50, self.y + 50, fill="green")
        c.create_text(self.x + 10, self.y + 10, text=int(self.g))
        c.create_text(self.x + 40, self.y + 10, text=int(self.h))
        c.create_text(self.x + 25, self.y + 30, text=int(self.f), font="arial 15 bold")

    def get_neighbours(self, x, y):
        self.neighbour_list.append([self.x - 50, self.y - 50])
        self.neighbour_list.append([self.x - 50, self.y])
        self.neighbour_list.append([self.x - 50, self.y + 50])

        self.neighbour_list.append([self.x, self.y - 50])
        self.neighbour_list.append([self.x, self.y + 50])

        self.neighbour_list.append([self.x + 50, self.y - 50])
        self.neighbour_list.append([self.x + 50, self.y])
        self.neighbour_list.append([self.x + 50, self.y + 50])

        print(self.neighbour_list)


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
    b_clear = Button(c, text="Clear", command=mainboard)
    b_clear.configure(width = 10, relief = FLAT)
    b_clear_window = c.create_window(300, 20, anchor=CENTER, window=b_clear)
    b_start = Button(c, text="Start", command=main)
    b_start.configure(width = 10, relief = FLAT)
    b_start_window = c.create_window(500, 20, anchor=CENTER, window=b_start)


def main():
    # There is no A, B or both points on the screen
    if not a_point_pos or not b_point_pos:
        print("Missing point(s)")
    else:
        a_node = Node(a_point_pos[0], a_point_pos[1])
        b_node = Node(b_point_pos[0], b_point_pos[1])
        open_l.append([a_node.x, a_node.y])
        print(open_l)
        current = a_point_pos
        list_control = 0
        while current != b_point_pos:
            current = open_l[list_control] # TODO: add logic to choose value from list that has the lowest f_cost
            closed_l.append(current)
            node = Node(current[0], current[1])
            print(node.neighbour_list)
            current_g = node.get_g_cost(current[0], current[1])
            current_h = node.get_h_cost(current[0], current[1])
            current_f = node.get_f_cost(current[0], current[1])
            node.draw_node(current[0], current[1], current_g, current_h, current_f)
            list_control += 1
            node.get_neighbours(current[0], current[1])
            break


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
    print(f"A point: {a_point_pos}")
    print(f"B point: {b_point_pos}")
    print(f"Walls: {walls_pos}")
    print("")


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
    print(f"A point: {a_point_pos}")
    print(f"B point: {b_point_pos}")
    print(f"Walls: {walls_pos}")
    print("")


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
    print(f"A point: {a_point_pos}")
    print(f"B point: {b_point_pos}")
    print(f"Walls: {walls_pos}")
    print("")

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
