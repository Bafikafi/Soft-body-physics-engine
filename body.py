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

    def __init__(self, x, y, velocty: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = velocty

    @abstractmethod
    def update(self):
        pass


class vertex(body):
    def next_render(self):
        physics.apply_gravity_force(self)
        self.position += self.velocity * consts.DELTA


class spring_edge:
    vertex_a = None
    vertex_b = None
    length = None
    stiffness = 1

    def __init__(self, vertex_a, vertex_b, length=20, stiffness=1) -> None:
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b
        self.length = length
        self.stiffness = stiffness

    def next_render(self):
        physics.apply_spring_forces(self)


class soft_body:
    springs: list(spring_edge) = []
    vertecies: list(vertex) = []

    def add_vertex(self, vertex: vertex):
        self.vertecies.append(vertex)

    def add_spring(self, spring: spring_edge):
        self.springs.append(spring)

    def update(self):
        for vertex in self.vertecies:
            vertex.update()


class blobik(soft_body):
    pass


class long_boi(soft_body):
    pass


class rigid_object_rectangle(body):
    width = 0
    height = 0

    def __init__(
        self, x, y, velocity: pygame.Vector2, width: float, height: float
    ) -> None:
        super().__init__(x, y, velocity)
        self.width = width
        self.height = height
