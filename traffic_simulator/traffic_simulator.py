import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 2700
SCREEN_HEIGHT = 1100
NUM_LANES = 4  # Adjust the number of lanes here
LANE_HEIGHT = SCREEN_HEIGHT // NUM_LANES
CAR_WIDTH = 100  # Fixed width of cars
MIN_CAR_LENGTH = 70
MAX_CAR_LENGTH = 150
MIN_CAR_SPEED = 1.8
MAX_CAR_SPEED = 3
SPAWN_INTERVAL = 100  # Frames between spawning cars
SAFE_DISTANCE = 100  # Safe distance between cars

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Highway Simulation")

clock = pygame.time.Clock()

class Car:
    def __init__(self, x, y, speed, length):
        self.width = CAR_WIDTH
        self.length = length
        self.x = x
        self.y = y
        self.speed = speed
        self.color = BLACK

    def move(self):
        self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, self.width))

def spawn_initial_cars():
    initial_cars = []
    for lane in range(NUM_LANES):
        speed = random.uniform(MIN_CAR_SPEED, MAX_CAR_SPEED)
        length = random.randint(MIN_CAR_LENGTH, MAX_CAR_LENGTH)
        initial_cars.append(Car(0, lane * LANE_HEIGHT + (LANE_HEIGHT - CAR_WIDTH) // 2, speed, length))
    return initial_cars

def check_collision(car, other_cars):
    for other_car in other_cars:
        if car != other_car and car.y < other_car.y + other_car.width and car.y + car.width > other_car.y:
            distance = other_car.x - (car.x + car.length)
            if 0 < distance < SAFE_DISTANCE:
                return min(other_car.speed, car.speed)
    return car.speed

cars = spawn_initial_cars()

frame_count = 0
running = True
while running:
    screen.fill(WHITE)

    # Draw lane lines
    for i in range(1, NUM_LANES):
        pygame.draw.line(screen, BLACK, (0, i * LANE_HEIGHT), (SCREEN_WIDTH, i * LANE_HEIGHT), 5)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn cars
    if frame_count % SPAWN_INTERVAL == 0:
        lane = random.randint(0, NUM_LANES - 1)
        speed = random.uniform(MIN_CAR_SPEED, MAX_CAR_SPEED)
        length = random.randint(MIN_CAR_LENGTH, MAX_CAR_LENGTH)
        cars.append(Car(0, lane * LANE_HEIGHT + (LANE_HEIGHT - CAR_WIDTH) // 2, speed, length))

    # Move and draw cars
    for car in cars:
        car_speed = check_collision(car, cars)
        car.move()
        car.speed = car_speed
        car.draw()

    # Remove cars that have passed the screen
    cars = [car for car in cars if car.x < SCREEN_WIDTH]

    pygame.display.flip()
    frame_count += 1
    clock.tick(60)

pygame.quit()
