import pygame
import consts

GRAVITY_ACCELERATION = 700



def apply_gravity_force(obj):
    obj.velocity.y += GRAVITY_ACCELERATION * consts.DELTA


def apply_spring_forces(edge):
    vertex_a = edge.vertex_a
    vertex_b = edge.vertex_b  # less typing
    a_vector: pygame.Vector2 = vertex_a.position
    b_vector: pygame.Vector2 = vertex_b.position

    spring_vector = b_vector - a_vector
    spring_vector_norm = spring_vector.normalize()
    spring_force_vector = (
        spring_vector.normalize()
        * (spring_vector.length() - edge.length)
        * edge.stiffness
        # * consts.SPRING_MULT
    )
    damping_force = (
        consts.DAMPER
        * ((vertex_b.velocity - vertex_a.velocity).dot(spring_vector_norm))
        * spring_vector_norm
    )
    edge.vertex_a.velocity += (
        spring_force_vector * consts.DELTA + damping_force * consts.DELTA
    )
    edge.vertex_b.velocity -= (
        spring_force_vector * consts.DELTA + damping_force * consts.DELTA
    )
