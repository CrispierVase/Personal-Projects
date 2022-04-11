#!/usr/bin/python3
import pyglet
import random
from math import sqrt
import time

width, height = 600, 600
window = pyglet.window.Window(width=width, height=height)
target_size = 25
num_of_targets = 10
score = 0
start = time.perf_counter()
batch = pyglet.graphics.Batch()


class Spot:
    def __init__(self, x, y):
        self.x = x - (target_size // 2)
        self.y = y - (target_size // 2)
        self.circle = pyglet.shapes.Circle(self.x, self.y, target_size, color=(255, 0, 0), batch=batch)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global score
    if button == pyglet.window.mouse.LEFT:
        for idx, place in enumerate(test):
            if sqrt((abs(x - place.x) ** 2) + (abs(y - place.y) ** 2)) <= target_size:
                del test[idx]
                test.append(Spot(random.randrange(int(target_size * 1.5), width - int(target_size * 1.5)), random.randrange(int(target_size * 1.5), height - int(target_size * 1.5))))
                score += 1


test = [Spot(random.randrange(int(target_size * 1.5), width - int(target_size * 1.5)), random.randrange(int(target_size * 1.5), height - int(target_size * 1.5))) for _ in range(num_of_targets)]

@window. event
def on_draw():
    window.clear()
    batch.draw()
    pyglet.text.Label(f'{score}',
                          font_name='Times New Roman',
                          font_size=20,
                          x=10*len(str(score)), y=height-20,
                          anchor_x='center', anchor_y='center').draw()

def update(*kwargs):
    print(*kwargs, 'whatever')
    pyglet.text.Label(str(f'{time.perf_counter() - start}'.split('.')[0]),
                          font_name='Times New Roman',
                          font_size=20,
                          x=10*len(str(f'{time.perf_counter() - start}'.split('.')[0])), y=height-40,
                          anchor_x='center', anchor_y='center').draw()
pyglet.app.run()