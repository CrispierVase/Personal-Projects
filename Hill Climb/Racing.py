import random
import pygame
import keyboard
distance = 2
ground = []
win = pygame.display.set_mode((400, 400))
win.fill((0, 0, 0))
variation = 1
car_width = 15
car_height = round(0.75 * car_width)


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0

    def show(self):
        pygame.draw.rect(win, (255, 255, 255), pygame.Rect(self.x, self.y, car_width, car_height))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), 2, 5)
        pygame.display.update()


ground.append(Point(0, win.get_width()))


def get_new_point(point):
    new_point_x = point.x
    new_point_y = point.y
    new_point_x += distance
    new_point_y -= random.randint(-variation, variation)
    if new_point_y > win.get_height():
        new_point_y = win.get_height() - 4 * variation
    elif new_point_y < 0:
        new_point_y = 0 + 4 * variation
    return Point(new_point_x, new_point_y)


i = 0
while ground[-1].x < win.get_width():
    if i == 1:
        ground.append(get_new_point(ground[0]))
    else:
        ground.append(get_new_point(ground[i]))
    i += 1

ground_points = [(point.x, point.y) for point in ground]
ground_line = pygame.draw.aalines(win, (255, 255, 255), False, ground_points)
pygame.display.update()
clock = pygame.time.Clock()
framerate = 10
cars = [Car(200, 200)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)
    win.fill((0, 0, 0))
    for car in cars:
        car.show()
    if keyboard.is_pressed('a'):
        cars[0].x -= distance
        for _ in range(framerate):
            ground.append(get_new_point(ground[-1]))
    clock.tick(10)
    for point in ground:
        point.x -= framerate
    ground_points = [(point.x, point.y) for point in ground]
    pygame.draw.aalines(win, (255, 255, 255), False, ground_points)
    pygame.display.update()
    for idx, point in enumerate(ground):
        if point.x < 0:
            del ground[idx]
