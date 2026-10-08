class vertex:
    position = None
    velocity = 0

    def __init__(self, x, y) -> None:
        self.position = (x, y)


class spring_edge:
    vertex_a = None
    vertex_b = None

    def __init__(self, vertex_a, vertex_b) -> None:
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b


class blob:
    ...
