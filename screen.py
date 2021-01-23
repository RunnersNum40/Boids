# import pyglet
# from pyglet.gl import *

# win = pyglet.window.Window()
# glClear(GL_COLOR_BUFFER_BIT)
# @win.event
# def on_draw():
#     glBegin(GL_POINTS)

from vectors import Vector
import math
import sys

import pygame
pygame.init()
pygame.display.set_caption('Boids')
clock = pygame.time.Clock()

class Screen:
    """A class that manages the rendering of boid objects"""
    def __init__(self, width, height, fps=60):
        self.fps = fps
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.middle = Vector(self.width, self.height)/2

    def draw(self, flock):
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit();

        clock.tick(self.fps)
        self.screen.fill((40, 44, 52))
        for boid in flock:
            tip = tuple((Vector.from_dir(boid.velo.angle, 8)+boid.pos+self.middle).vec)
            left = tuple((Vector.from_dir(boid.velo.angle-math.pi/1.5, 4)+boid.pos+self.middle).vec)
            right = tuple((Vector.from_dir(boid.velo.angle+math.pi/1.5, 4)+boid.pos+self.middle).vec)
            pygame.draw.polygon(self.screen, (85, 140, 244), (tip, left, right))
        pygame.display.update()



try:
    pass
finally:
    pygame.quit()