import pygame
import consts

GRAVITY_ACCELERATION = 800


def apply_gravity_force(obj):
    obj.velocity.y += GRAVITY_ACCELERATION * consts.DELTA


def apply_spring_forces(edge):
    vertex_a = edge.vertex_a
    vertex_b = edge.vertex_b  # less typing
    a_vector = vertex_a.position
    b_vector = vertex_b.position

    total_vector = pygame.Vector2(b_vector.x - a_vector.x, b_vector.y - a_vector.y)
    force_vector = (
        total_vector.normalize()
        * (total_vector.length() - edge.length)
        * edge.stiffness
        * 30
    )
    edge.vertex_a.velocity = pygame.Vector2(
        vertex_a.velocity.x
        + (force_vector.x * consts.DELTA - vertex_a.velocity.x * consts.DAMPER),
        vertex_a.velocity.y
        + (force_vector.y * consts.DELTA - vertex_a.velocity.y * consts.DAMPER),
    )
    edge.vertex_b.velocity = pygame.Vector2(
        vertex_b.velocity.x
        - (force_vector.x * consts.DELTA - vertex_b.velocity.x * consts.DAMPER),
        vertex_b.velocity.y
        - (force_vector.y * consts.DELTA - vertex_b.velocity.y * consts.DAMPER),
    )
