from __future__ import annotations
from math import copysign
import pygame
import consts

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from body import spring_edge, vertex
    from collision_detection import point_collider


GRAVITY_ACCELERATION = 700


def apply_gravity_force(obj):
    obj.velocity.y += GRAVITY_ACCELERATION * consts.DELTA


def apply_spring_forces(edge: spring_edge):
    vertex_a = edge.vertex_a
    vertex_b = edge.vertex_b  # less typing
    a_vector: pygame.Vector2 = vertex_a.position
    b_vector: pygame.Vector2 = vertex_b.position

    spring_vector = b_vector - a_vector
    spring_force_vector = calculate_spring_force(edge)
    spring_vector_norm = spring_vector.normalize()
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


def calculate_spring_force(edge: spring_edge):
    vertex_a = edge.vertex_a
    vertex_b = edge.vertex_b
    a_vector: pygame.Vector2 = vertex_a.position
    b_vector: pygame.Vector2 = vertex_b.position

    spring_vector = b_vector - a_vector
    spring_force_vector = (
        spring_vector.normalize()
        * (spring_vector.length() - edge.length)
        * edge.stiffness
    )
    return spring_force_vector


def apply_friction(vertex: vertex, normal: pygame.Vector2):
    total_force = pygame.Vector2(0, GRAVITY_ACCELERATION * consts.DELTA)
    for spring in vertex.springs:
        total_force += calculate_spring_force(spring)
    normal_force = total_force.dot(normal)
    friction_force = abs(normal_force * consts.FRICTION_CONSTANT)
    rotated_normal = pygame.Vector2(-normal.y, normal.x)
    vel = vertex.velocity
    vertex.velocity.x = copysign(
        max(0, abs(vel.x) - abs(rotated_normal.x) * friction_force * consts.DELTA),
        vel.x,
    )  # Mass is 1
    vertex.velocity.y = copysign(
        max(0, abs(vel.y) - abs(rotated_normal.y) * friction_force * consts.DELTA),
        vel.y,
    )
