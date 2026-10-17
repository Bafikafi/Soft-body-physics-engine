import pygame
from renderer import *
import body
import collision_detection
import sys
import consts
import softbody_factory


collision_detector = collision_detection.collision_detector()
test_body = softbody_factory.build("assets/double_ring.json", collision_detector)


test_body.vertecies[1].position.x += 15
ground = body.rigid_object_rectangle(250, 450, 900, 100)
ground.add_rect_collider(collision_detection.rect_collider(ground, collision_detector))
pygame.init()

display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
physics_steps = 8

while True:
    consts.DELTA = clock.tick(60) / (1000 * physics_steps)
    for _ in range(physics_steps):
        test_body.update()
        collision_detector.update()

    renderer.render_rigid_object(display, ground)
    renderer.render_debug(display, test_body.vertecies)
    renderer.redner_edge_debug(display, test_body.springs)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    display.fill((0, 0, 0))
