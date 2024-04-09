import tkinter as tk
import random


class Circle:
    def __init__(self, canvas, x, y, radius, color, number):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.number = number
        self.circle_id = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)
        self.text_id = canvas.create_text(x, y, text=str(number), fill='white')
        self.selected = False

    def draw(self):
        self.canvas.itemconfigure(self.circle_id, fill=self.color)
        self.canvas.itemconfigure(self.text_id, text=str(self.number))
        if self.selected:
            self.canvas.itemconfigure(self.circle_id, outline="red")
        else:
            self.canvas.itemconfigure(self.circle_id, outline="")


def check_collision(circle, existing_circles):
    for other_circle in existing_circles:
        distance = ((circle.x - other_circle.x) ** 2 + (circle.y - other_circle.y) ** 2) ** 0.5
        if distance < circle.radius + other_circle.radius + 10:  # Add padding to prevent overlap
            return True
    return False


def create_random_circle(canvas, player, existing_circles):
    while True:
        x = random.randint(100, 900)  # Random x-coordinate within canvas
        y = random.randint(100, 700)  # Random y-coordinate within canvas
        radius = random.randint(10, 40)  # Random radius
        number = random.randint(0, 50)  # Random number
        new_circle = Circle(canvas, x, y, radius, "gray", number)
        overlap = check_collision(new_circle, existing_circles)
        if not overlap:
            existing_circles.append(new_circle)
            new_circle.draw()
            break


def select_circle(event):
    global first_click

    for circle in existing_circles:
        distance = ((event.x - circle.x) ** 2 + (event.y - circle.y) ** 2) ** 0.5
        if distance < circle.radius:
            if first_click:
                if circle.color == "blue":
                    circle.selected = True
                    first_click = False
                    circle.draw()
                    break
            else:
                if circle.color != "blue":
                    if circle.selected:
                        circle.selected = False
                    else:
                        circle.selected = True
                    for other_circle in existing_circles:
                        other_circle.selected = False
                    circle.draw()
                    break


def transfer_units(event):
    global player, first_click

    first_click = True
    for circle in existing_circles:
        if circle.selected:
            for other_circle in existing_circles:
                distance = ((event.x - other_circle.x) ** 2 + (event.y - other_circle.y) ** 2) ** 0.5
                if distance < other_circle.radius and other_circle.color != "blue":
                    if circle.number > 0:
                        circle.number -= 1
                        other_circle.number += 1
                        circle.draw()
                        other_circle.draw()
                    break


def main():
    global player, canvas, existing_circles, first_click

    root = tk.Tk()
    root.title("Game")

    canvas = tk.Canvas(root, width=1000, height=800, bg='white')
    canvas.pack()

    player = Circle(canvas, 500, 400, 20, "blue", 100)
    player.draw()

    existing_circles = []
    for _ in range(20):
        create_random_circle(canvas, player, existing_circles)

    canvas.bind("<Button-1>", select_circle)
    canvas.bind("<Button-3>", transfer_units)

    root.mainloop()


if __name__ == "__main__":
    main()



