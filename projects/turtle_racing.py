import turtle
import time
import random

class TurtleRacing:
    def __init__(self) -> None:
        self.WIDTH, self.HEIGHT = 500, 500
        self.COLORS = ["cyan", "red", "pink", "black", "blue", "yellow", "green", "brown"]

    def get_number_of_racers(self):
        racers = 0
        while True:
            racers = input("Enter the number of racers (2-10): ")
            if racers.isdigit():
                racers = int(racers)
            else:
                print("Please enter a number.")
                continue
            
            if 2 <= racers <= 10:
                return racers
            else:
                print("Please enter a number between 2 and 10.")
                continue

    def setup_game_environment(self):
        screen = turtle.Screen()
        screen.setup(self.WIDTH, self.HEIGHT)
        screen.title("Turtle Racing!")

    def build_turtle(self, i, num_of_racers, color="cyan"):
        racer = turtle.Turtle()
        racer.color(color)
        racer.speed(2)
        racer.shape("turtle")
        spacingx = - self.WIDTH // 2 + (i+1) * (self.WIDTH // (num_of_racers+1))
        spacingy = -self.HEIGHT // 2 + 20
        racer.left(90)
        racer.penup()
        racer.setpos(spacingx, spacingy)
        racer.pendown()
        return racer

    def race(self, objects):
        while True:
            for i, racer in enumerate(objects):
                distance = random.randrange(1,20)
                racer.forward(distance)

                x, y = racer.pos()
                if y >= self.HEIGHT // 2 -10:
                    time.sleep(4)
                    return i
        

def main():
    obj = TurtleRacing()
    num_of_racers = obj.get_number_of_racers()
    obj.setup_game_environment()

    colors = obj.COLORS[:num_of_racers]
    objects = []

    for i in range(num_of_racers):
        racer = obj.build_turtle(i, num_of_racers, color=colors[i])
        objects.append(racer)

    win_idx = obj.race(objects)
    print(f"{colors[win_idx]} turtle won!")

main()