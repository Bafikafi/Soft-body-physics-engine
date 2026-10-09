# importing pygame module
import pygame
from renderer import *
import soft_body_parts
import time
import physics

# importing sys module
import sys
import consts

vertex = [soft_body_parts.vertex(100, 100), soft_body_parts.vertex(200, 100)]
edge = soft_body_parts.spring_edge(vertex[0], vertex[1], 50)

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

    vertex[0].next_render()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
