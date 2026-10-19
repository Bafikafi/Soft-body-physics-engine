import pygame
from renderer import *
import body as Body
import collision_detection
import sys
import consts
import softbody_factory
from mouse_interaction import mouse_drag

collision_detector = collision_detection.collision_detector()
test_body = softbody_factory.build("assets/double_ring.json", collision_detector)


ground = Body.rigid_object_rectangle(250, 750, 1500, 100)
ground.add_rect_collider(collision_detection.rect_collider(ground, collision_detector))
pygame.init()
bodies = [test_body, ground]

display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
physics_steps = 8
interaction = None
while True:
    consts.DELTA = clock.tick(60) / (1000 * physics_steps)
    for _ in range(physics_steps):
        for body in bodies:
            body.update()
        collision_detector.update()

    renderer.render_rigid_object(display, ground)
    renderer.render_debug(display, test_body.vertecies)
    renderer.redner_edge_debug(display, test_body.springs)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = pygame.Vector2(mouse_pos)
            if interaction == None:
                v = test_body.get_closest_point(mouse_pos)
                interaction = mouse_drag(mouse_pos, v)

        if event.type == pygame.MOUSEBUTTONUP:
            interaction.release()
            interaction = None
    if interaction is not None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pygame.Vector2(mouse_pos)
        for _ in range(physics_steps):
            interaction.update(mouse_pos)

    pygame.display.update()
    display.fill((0, 0, 0))
