# importing pygame module
import pygame
from renderer import *
import body
import time
import physics

# importing sys module
import sys
import consts

vertex = [body.vertex(150, 100), body.vertex(150, 200)]
edge = body.spring_edge(vertex[0], vertex[1], 50)

# initialising pygame
pygame.init()

# creating display
display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
# creating a running loop
while True:
    # creating a loop to check events that
    # are occuring
    consts.DELTA = clock.tick(60) / 1000
    display.fill((0, 0, 0))
    edge.next_render()
    renderer.redner_edge_debug(display, edge)
    renderer.render_debug(display, vertex)

    # TODO Later stages, every vertex shall have its own physics
    # for vert in vertex:
    #   vert.next_render()

    vertex[0].update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
