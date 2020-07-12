
import queue
from tkinter import *

root = Tk()
root.title("Path finding algorithm")
root.geometry("800x800")
root.resizable(False,False)

c = Canvas(root, width=800, height=800, background="#E4E4E4")
c.pack()


def mainboard():
    for i in range(14):
        for j in range(14):
            c.create_rectangle(j * 50 + 50, i * 50 + 50, j * 50 + 100, i * 50 + 100)


def square_clicked(x, y):
    x_minus = x % 50
    x -= x_minus
    y_minus = y % 50
    y -= y_minus
    return x, y


def square_erease(x, y):
    c.create_rectangle(x, y, x + 50, y + 50, fill="#E4E4E4")


def square_overlap(x, y, type):
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


a_point_pos = []
b_point_pos = []
walls_pos = []

mainboard()


c.bind("<1>", create_a)
c.bind("<2>", create_wall)
c.bind("<3>", create_b)

root.mainloop()
c.mainloop()
