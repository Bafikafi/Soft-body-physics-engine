import physics
import consts
import pygame


class vertex:
    position = None
    velocity = pygame.Vector2(float(0), float(0))

    def __init__(
        self,
        x=0,
        y=0,
    ) -> None:
        self.position = pygame.Vector2(float(x), float(y))

    def next_render(self):
        physics.apply_gravity_force(self)

        self.position += self.velocity * consts.DELTA


class spring_edge:
    vertex_a = None
    vertex_b = None

    def __init__(self, vertex_a, vertex_b) -> None:
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b


class blob:
    ...
