
import random
import tkinter as tk


class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=1000, height=800, bg='white')
        self.canvas.pack()

        self.player = Circle(self.canvas, 500, 400, 20, "blue", 100)
        self.player.draw()

        self.existing_circles = [self.player]
        for _ in range(20):
            self.existing_circles.append(Circle(self.canvas, random.randint(100, 900), random.randint(100, 700), 20, "gray", random.randint(1,50)))
            self.existing_circles[-1].draw()

        self.selected_circle = None

        self.root.bind("<Button-1>", self.select_circle)

    def select_circle(self, event):
        for circle in self.existing_circles:
            distance = ((event.x - circle.x) ** 2 + (event.y - circle.y) ** 2) ** 0.5
            if distance < circle.radius:
                if self.selected_circle is None:
                    if circle.color == "blue":
                        self.selected_circle = circle
                    else:
                        if circle.number > 0:
                            if self.selected_circle is not None:
                                self.selected_circle.number -= 1
                                circle.number -= 1
                                self.selected_circle.draw()
                                circle.draw()
                                self.selected_circle = None
                else:
                    if circle.color != "blue" and circle != self.selected_circle:
                        self.selected_circle.number -= 1
                        circle.number -= 1
                        self.selected_circle.draw()
                        circle.draw()
                        self.selected_circle = None
                        if circle.number == 0:
                            circle.color = "blue"
                            circle.canvas.itemconfigure(circle.circle_id, fill=circle.color)
                            self.selected_circle = circle
                break

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


root = tk.Tk()
root.title("Game")
game = Game(root)
root.mainloop()


