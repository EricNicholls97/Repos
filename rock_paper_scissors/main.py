import tkinter as tk
from PIL import Image, ImageTk
from enum import Enum
import random
import math
import time


class Type(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3


UNIT_SIZE = 30
# WIDTH = 1000
# HEIGHT = 900
RADIUS = 600


rock_score = 0
paper_score = 0
scissors_score = 0

NUM_PLAYERS = 40
TIME_WAIT = 7

SPEED = 7

# Define the barrier circles as a list of tuples (x, y, radius)
barriers = [
    (RADIUS, RADIUS, 113),  # Center circle
    (RADIUS + 200, RADIUS - 100, 50),  # Example: Circle at (x=RADIUS+200, y=RADIUS-100) with radius 100
    (RADIUS - 150, RADIUS + 150, 50)   # Example: Circle at (x=RADIUS-150, y=RADIUS+150) with radius 80
]
NUM_TINY_CIRCLES = 30
TINY_CIRCLE_RADIUS = 10
angle_between_circles = 2 * math.pi / NUM_TINY_CIRCLES
tiny_circles = []
for i in range(NUM_TINY_CIRCLES):
    angle = i * angle_between_circles
    x_circle = RADIUS + (RADIUS - TINY_CIRCLE_RADIUS) * math.cos(angle)
    y_circle = RADIUS + (RADIUS - TINY_CIRCLE_RADIUS) * math.sin(angle)
    tiny_circles.append((x_circle, y_circle, TINY_CIRCLE_RADIUS))
barriers.extend(tiny_circles)

class Game(tk.Tk):
    def __init__(self):
        global rock_score, paper_score, scissors_score
        super().__init__()

        self.title("Rock Paper Scissors")
        self.canvas = tk.Canvas(self, width=RADIUS * 2, height=RADIUS * 2, bg='black')
        self.canvas.pack()

        self.canvas.create_oval(0, 0, RADIUS * 2, RADIUS * 2, fill="white", outline="black")

        # Load images after Tkinter root window has been initialized
        rock_img = Image.open("rock.png").resize((UNIT_SIZE, UNIT_SIZE), Image.ANTIALIAS)
        paper_img = Image.open("paper.png").resize((UNIT_SIZE, UNIT_SIZE), Image.ANTIALIAS)
        scissors_img = Image.open("scissors.png").resize((UNIT_SIZE, UNIT_SIZE), Image.ANTIALIAS)

        # Draw barrier circles
        for barrier in barriers:
            x, y, radius = barrier
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="black", fill="black")

        self.images = {
            Type.ROCK: ImageTk.PhotoImage(rock_img),
            Type.PAPER: ImageTk.PhotoImage(paper_img),
            Type.SCISSOR: ImageTk.PhotoImage(scissors_img)
        }

        self.units = []

        for typ in [Type.ROCK, Type.PAPER, Type.SCISSOR]:
            for i in range(NUM_PLAYERS):
                angle = random.uniform(0, 2 * math.pi)
                r1 = random.uniform(0, RADIUS - UNIT_SIZE / 2)
                r2 = random.uniform(0, RADIUS - UNIT_SIZE / 2)
                x = RADIUS + r1 * math.cos(angle)
                y = RADIUS + r2 * math.sin(angle)
                unit = Unit(typ, x, y)
                self.units.append(unit)

        # Create a label for the scoreboard
        self.scoreboard_label = tk.Label(self, text=f"ROCK: {rock_score}     PAPER: {paper_score}   SCISSORS: {scissors_score}", font=("Arial", 16))
        self.scoreboard_label.place(relx=0.6, rely=0.99, anchor="se")

        self.each_type = {Type.ROCK: NUM_PLAYERS, Type.PAPER: NUM_PLAYERS, Type.SCISSOR: NUM_PLAYERS}

        self.current_counts_label = tk.Label(self, text=f"Rock: {self.each_type[Type.ROCK]}\n\nPaper: {self.each_type[Type.PAPER]}\n\nScissors: {self.each_type[Type.SCISSOR]}\n")
        self.current_counts_label.place(relx=0.058, rely=0.5, anchor="se")

        self.winner_banner = tk.Label(self, text=f"")
        self.winner_banner.place(relx=0.99, rely=0.5, anchor="se")

        self.display()  # Display the units initially
        self.move()  # Start moving the units

    def display(self):
        self.canvas.delete("unit")  # Clear previously displayed units
        for unit in self.units:
            # Create a rectangle
            rectangle_id = self.canvas.create_rectangle(unit.x - UNIT_SIZE/2, unit.y - UNIT_SIZE/2, unit.x + UNIT_SIZE/2, unit.y + UNIT_SIZE/2, fill="white", outline="black", tags="unit")
            # Place the image inside the rectangle
            self.canvas.create_image(unit.x, unit.y, anchor=tk.CENTER, image=self.images[unit.type], tags="unit")

    def move(self):
        for unit in self.units:
            nearest_unit, prey = self.find_nearest_unit(unit)
            if nearest_unit is None:
                continue
            x_diff = nearest_unit.x - unit.x
            y_diff = nearest_unit.y - unit.y
            c2 = math.sqrt(x_diff ** 2 + y_diff ** 2)

            if not prey:
                x_diff *= -1
                y_diff *= -1

            # Calculate the new position
            new_x = unit.x + SPEED * x_diff / c2
            new_y = unit.y + SPEED * y_diff / c2

            # Calculate the distance from the center of the circular canvas
            distance_from_center = math.sqrt((new_x - RADIUS) ** 2 + (new_y - RADIUS) ** 2)

            # If the new position is outside the circular boundary, adjust it to stay within the boundary
            if distance_from_center > RADIUS - UNIT_SIZE / 2:
                angle = math.atan2(new_y - RADIUS, new_x - RADIUS)
                new_x = RADIUS + (RADIUS - UNIT_SIZE / 2) * math.cos(angle)
                new_y = RADIUS + (RADIUS - UNIT_SIZE / 2) * math.sin(angle)

            # Ensure the new position does not enter any barrier circle
            for barrier in barriers:
                barrier_x, barrier_y, barrier_radius = barrier
                distance_from_barrier = math.sqrt((new_x - barrier_x) ** 2 + (new_y - barrier_y) ** 2)
                if distance_from_barrier < barrier_radius + UNIT_SIZE / 2:
                    # Adjust position to prevent entering the barrier circle
                    angle = math.atan2(new_y - barrier_y, new_x - barrier_x)
                    new_x = barrier_x + (barrier_radius + UNIT_SIZE / 2) * math.cos(angle)
                    new_y = barrier_y + (barrier_radius + UNIT_SIZE / 2) * math.sin(angle)
                    break  # Stop checking other barriers if intersection found

            unit.x = new_x
            unit.y = new_y

        self.each_type = {Type.ROCK: 0, Type.PAPER: 0, Type.SCISSOR: 0}
        for unit in self.units:
            self.each_type[unit.type] += 1

            for other_unit in self.units:
                if unit == other_unit:
                    continue

                # Calculate the distance between units
                distance = math.sqrt((unit.x - other_unit.x) ** 2 + (unit.y - other_unit.y) ** 2)

                # Check for collision
                if distance < UNIT_SIZE:
                    # Move the units apart
                    overlap = UNIT_SIZE - distance
                    angle = math.atan2(unit.y - other_unit.y, unit.x - other_unit.x)
                    unit.x += overlap / 2 * math.cos(angle)
                    unit.y += overlap / 2 * math.sin(angle)
                    other_unit.x -= overlap / 2 * math.cos(angle)
                    other_unit.y -= overlap / 2 * math.sin(angle)

                    # Handle type switching if there's a collision
                    if unit.type == Type.ROCK:
                        if other_unit.type == Type.SCISSOR:
                            other_unit.type = Type.ROCK
                        elif other_unit.type == Type.PAPER:
                            unit.type = Type.PAPER

                    elif unit.type == Type.PAPER:
                        if other_unit.type == Type.ROCK:
                            other_unit.type = Type.PAPER
                        elif other_unit.type == Type.SCISSOR:
                            unit.type = Type.SCISSOR

                    elif unit.type == Type.SCISSOR:
                        if other_unit.type == Type.PAPER:
                            other_unit.type = Type.SCISSOR
                        elif other_unit.type == Type.ROCK:
                            unit.type = Type.ROCK

        self.display()  # Redraw the canvas with updated unit positions

        self.check_game_state_and_restart()

        self.after(10, self.move)  # Schedule the move method to be called again after 20 milliseconds

    def find_nearest_unit(self, this_unit):
        nearest_unit = None
        min_distance = float('inf')

        for potential_unit in self.units:

            prey = None
            if this_unit == potential_unit:  # Exclude the target unit itself
                continue

            if this_unit.type == potential_unit.type:
                continue

            if this_unit.type == Type.SCISSOR:
                prey = True if potential_unit.type == Type.PAPER else False
            elif this_unit.type == Type.PAPER:
                prey = True if potential_unit.type == Type.ROCK else False
            elif this_unit.type == Type.ROCK:
                prey = True if potential_unit.type == Type.SCISSOR else False

            distance = math.sqrt((this_unit.x - potential_unit.x) ** 2 + (this_unit.y - potential_unit.y) ** 2)

            if distance < min_distance:
                min_distance = distance
                nearest_unit = potential_unit
                nearest_prey = prey

        return nearest_unit, nearest_prey   # return nearest unit and wheteher its prey (True=prey, False=predator)


    def check_game_state_and_restart(self):
        global rock_score, paper_score, scissors_score

        # Create a label for the scoreboard
        self.current_counts_label.config(
            text=f"Rock: {self.each_type[Type.ROCK]}\nPaper: {self.each_type[Type.PAPER]}\nScissors: {self.each_type[Type.SCISSOR]}\n",
            font=("Arial", 16))

        if self.each_type[Type.ROCK] == 0:
            scissors_score += 1
            winner = "SCISSORS"

        elif self.each_type[Type.PAPER] == 0:
            rock_score += 1
            winner = "ROCK"

        elif self.each_type[Type.SCISSOR] == 0:
            paper_score += 1
            winner = "PAPER"

        else:
            return

        # game is over
        # change winner banner
        self.winner_banner.config(text=f"{winner} checkmates!", font=("Arial", 16))
        self.update_idletasks()

        # Create a label for the scoreboard
        self.scoreboard_label.config(text=f"ROCK: {rock_score}\t\tPAPER: {paper_score}\t\tSCISSORS: {scissors_score}", font=("Arial", 16))

        time.sleep(TIME_WAIT)


        self.winner_banner.config(text="")

        # If all types are the same, clear the canvas and restart the game
        self.canvas.delete("unit")
        self.units.clear()

        # Reset units with random positions and types
        for typ in [Type.ROCK, Type.PAPER, Type.SCISSOR]:
            for i in range(NUM_PLAYERS):
                angle = random.uniform(0, 2 * math.pi)
                r1 = random.uniform(0, RADIUS - UNIT_SIZE / 2)
                r2 = random.uniform(0, RADIUS - UNIT_SIZE / 2)
                x = RADIUS + r1 * math.cos(angle)
                y = RADIUS + r2 * math.sin(angle)
                unit = Unit(typ, x, y)
                self.units.append(unit)


class Unit:
    def __init__(self, typ, x, y):
        self.type = typ
        self.x = x
        self.y = y


if __name__ == "__main__":
    root = Game()  # Create the Tkinter root window
    root.mainloop()  # Start the mainloop for the root window
