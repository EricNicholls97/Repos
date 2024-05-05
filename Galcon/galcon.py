
import random
import tkinter as tk


class Game:
    """This class represents the game itself, and contains the main
    game loop, as well as the game's user interface and behavior.
    """
    def __init__(self, root):
        """
        Constructor for the Game class
        Parameters:
            root (Tk): The root tkinter object for the game
        """
        self.width = 2000
        self.height = 1200

        self.number_of_neutrals = 20

        self.root = root
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()

        self.click_amount = 0.5

        # Create the player circle
        self.player = Circle(self.canvas, self.width, self.height, "blue")
        self.player.draw()


        # Create the AI red initial circle
        self.ai_red = [Circle(self.canvas, self.width, self.height, "red")]
        self.ai_red[0].draw()

        # List of all circles in the game, including the player
        self.existing_circles = [self.player, self.ai_red[0]]

        # Add some random circles to the game
        for _ in range(self.number_of_neutrals):
            self.existing_circles.append(Circle(self.canvas, self.width, self.height))
            self.existing_circles[-1].draw()

        # Currently selected circle
        self.selected_circle = None

        # Add a binding to the left mouse button for selecting circles
        self.root.bind("<Button-1>", self.select_circle)
        
        self._schedule_ai_selection(self.ai_red[0], 0)
        

    def select_circle(self, event):
        """
        Selects a circle when the left mouse button is pressed
        Parameters:
            event (Event): The event object generated by the mouse click
        """

        for circle in self.existing_circles:
            distance = ((event.x - circle.x) ** 2 + (event.y - circle.y) ** 2) ** 0.5
            if distance < circle.radius:
                if self.selected_circle is None:
                    if circle.color == "blue":
                        self.selected_circle = circle
                else:
                    if circle.color == "gray" and circle != self.selected_circle:
                        amount = int(self.selected_circle.number * self.click_amount)
                        self.selected_circle.number -= amount
                        circle.number -= amount
                        if circle.number <= 0:
                            circle.number *= -1
                            circle.color = self.selected_circle.color
                            circle.canvas.itemconfigure(circle.circle_id, fill=circle.color)
                            circle._schedule_increment(0)
                        self.selected_circle.draw()
                        circle.draw()
                        self.selected_circle = None
                break


    def _schedule_ai_selection(self, circle, i):
        """ Every 1/2 second, randomly select a circle to attack """
        
        planets_excluding_mine = [circ for circ in self.existing_circles if circ.color != circle.color]
        circle_to_attack = random.choice(planets_excluding_mine)
        
        amount = circle.number // 2
        circle.number -= amount
        circle_to_attack.number -= amount
        if circle_to_attack.number <= 0:    # planet is captured and under ai control
            circle_to_attack.number *= -1
            circle_to_attack.color = circle.color
            circle_to_attack.canvas.itemconfigure(circle_to_attack.circle_id, fill=circle_to_attack.color)
            circle_to_attack._schedule_increment(0)
            self.ai_red.append(circle_to_attack)

        circle.draw()
        circle_to_attack.draw()
        
        for c in self.ai_red:
            self.canvas.after(1000, self._schedule_ai_selection, c, i+1)


class Circle:
    """ This class represents a circle on the game board """
    def __init__(self, canvas, max_x, max_y, color=None):
        """
        Constructor for the Circle class
        Parameters:
            canvas (Canvas): The canvas object on which to draw the circle
            max_x (int): The maximum x-coordinate
            max_y (int): The maximum y-coordinate
        """
        self.canvas = canvas
        self.x = random.randint(0, max_x)
        self.y = random.randint(0, max_y)
        self.radius = random.randint(10, 30)
        self.number = random.randint(1, 50)
        self.color = "gray"
        if color != None:
            self.color = color
            self.radius = 30
            self.number = 100
        self.circle_id = canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill=self.color)
        self.text_id = canvas.create_text(self.x, self.y, text=str(self.number), fill='white')
        self.selected = False

        if color != None:
            self._schedule_increment(0)
    

    def _schedule_increment(self, i):       
        """ Every 1/4 second, increment this number based on its radius. Highest radius increments every time. Lower radius increments every 4 times"""
        increment_lookup = { (28, 30): 3, 
                             (24, 27): 4,
                             (20, 23): 5,
                             (15, 19): 6,
                             (10, 14): 7 }
        
        for key in increment_lookup.keys():
            if key[0] <= self.radius <= key[1]:
                increme = increment_lookup[key]
                break
        
        if i % increme == 0:
            self.number += 1
            self.canvas.itemconfigure(self.text_id, text=str(self.number))
        
        self.canvas.after(250, self._schedule_increment, i+1)


    def draw(self):
        """ Redraws the circle on the canvas"""
        self.canvas.itemconfigure(self.circle_id, fill=self.color)
        self.canvas.itemconfigure(self.text_id, text=str(self.number))
        if self.selected:
            self.canvas.itemconfigure(self.circle_id, outline="red")
        else:
            self.canvas.itemconfigure(self.circle_id, outline="")


root = tk.Tk()
root.title("Galcon")
game = Game(root)
root.mainloop()





