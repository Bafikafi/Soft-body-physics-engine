from __future__ import annotations
import physics
import consts
import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import collision_detection


class body(ABC):
    position: pygame.Vector2 = None
    velocity: pygame.Vector2 = None

    def __init__(self, x, y, velocity: pygame.Vector2 | None = None) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0) if velocity is None else velocity.copy()

    @abstractmethod
    def update(self):
        pass


class vertex(body):

    def __init__(self, x, y, velocity: pygame.Vector2 | None = None) -> None:
        super().__init__(x, y, velocity)
        self.springs = list()

    def update(self):
        physics.apply_gravity_force(self)
        self.position += self.velocity * consts.DELTA

    def add_point_collider(self, collider: collision_detection.point_collider):
        self.collider = collider


class spring_edge:
    def __init__(self, vertex_a, vertex_b, length=20, stiffness=1) -> None:
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b
        self.length = length
        self.stiffness = stiffness

    def update(self):
        physics.apply_spring_forces(self)


# TODO - Refactor: why no softbody collider in softbody class?
class soft_body:
    def __init__(self) -> None:
        self.vertecies = list()
        self.springs = list()
        self.collider = None

    def add_vertex(self, vertex: vertex):
        self.vertecies.append(vertex)

    def add_spring(self, spring: spring_edge):
        self.springs.append(spring)

    def add_soft_body_collider(self, collider: collision_detection.soft_body_collider):
        self.collider = collider

    def update(self):
        for vertex in self.vertecies:
            vertex.update()
        for spring in self.springs:
            spring.update()


class blobik(soft_body):
    pass


class long_boi(soft_body):
    pass


class rigid_object_rectangle(body):
    width = 0
    height = 0

    def __init__(
        self,
        x,
        y,
        width: float,
        height: float,
        velocity: pygame.Vector2 = pygame.Vector2(0, 0),
    ) -> None:
        super().__init__(x, y, velocity)
        self.width = width
        self.height = height

    def add_rect_collider(self, collider: collision_detection.rect_collider):
        self.collider = collider

    def update(self):
        return super().update()
