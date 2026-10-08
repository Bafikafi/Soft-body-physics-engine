import physics
import consts


class vertex:
    position = None
    velocity = (0, 0)

    def __init__(self, x=0, y=0) -> None:
        self.position = (x, y)

    def next_render(self):
        physics.apply_gravity_force(self)

        pos = list(self.position)

        pos[0] += self.velocity[0] * consts.DELTA
        pos[1] += self.velocity[1] * consts.DELTA

        self.position = tuple(pos)


class spring_edge:
    vertex_a = None
    vertex_b = None

    def __init__(self, vertex_a, vertex_b) -> None:
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b


class blob:
    ...
