# importing pygame module
import pygame
from renderer import *
import body
import collision_detection
import time
import physics

# importing sys module
import sys
import consts

collision_detector = collision_detection.collision_detector()
vertex = [body.vertex(150, 100), body.vertex(200, 100)]
edge = body.spring_edge(vertex[0], vertex[1], 30, 20)
soft = body.soft_body()
for point in vertex:
    point.add_point_collider(collision_detection.point_collider(point))
    soft.add_vertex(point)
soft.add_spring(edge)
soft_collider = collision_detection.soft_body_collider(soft, collision_detector)
ground = body.rigid_object_rectangle(250, 450, 900, 100)
ground.add_rect_collider(collision_detection.rect_collider(ground, collision_detector))
print(soft_collider.body_colliders)
# initialising pygame
pygame.init()

# creating display
display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
consts.DELTA = clock.tick(60) / 1000
# creating a running loop
while True:
    # creating a loop to check events that
    # are occuring
    consts.DELTA = clock.tick(60) / 1000
    soft.update()
    collision_detector.update()
    renderer.render_rigid_object(display, ground)
    renderer.render_debug(display, vertex)
    renderer.redner_edge_debug(display, edge)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    display.fill((0, 0, 0))
