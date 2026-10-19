from pygame import Vector2
import body as Body

DRAG_STIFFNESS = 1000


class mouse_drag:
    def __init__(self, pos: Vector2, drag_vertex: Body.vertex) -> None:
        self.virtual_vertex = Body.hold_vertex(pos.x, pos.y)
        if self.virtual_vertex.position.distance_to(drag_vertex.position) > 30:
            return
        self.virtual_spring = Body.spring_edge(
            self.virtual_vertex, drag_vertex, 0, DRAG_STIFFNESS
        )

    def update(self, pos: Vector2) -> None:
        if not hasattr(self, "virtual_spring"):
            return
        self.virtual_vertex.set_target_posisiton(pos)
        self.virtual_vertex.velocity = Vector2(0, 0)
        self.virtual_spring.update()
        self.virtual_vertex.update()

    def release(self) -> None:
        if hasattr(self, "virtual_string"):
            self.virtual_spring.vertex_a = None
            self.virtual_spring.vertex_b = None
            del self.virtual_spring
        del self.virtual_vertex
