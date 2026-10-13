from __future__ import annotations
import pygame
from abc import ABC, abstractmethod
import body as Body


class collision_detector:
    pass  # TODO


class collider(ABC):
    def __init__(self, body: Body.body) -> None:
        self.body = body

    @abstractmethod
    def collided(self, other: "collider") -> bool:
        pass


class rect_collider(collider):
    def collided(self, other: "collider") -> bool:
        if isinstance(other, rect_collider):
            if not isinstance(other.body, Body.rigid_object_rectangle):
                raise Exception(
                    "Could not find recatnge rigid body"
                )  # TODO fix later, not needed for product
        if isinstance(other, point_collider):
            is_in_horizontal = (
                self.body.position.x + self.body.width
                >= other.body.position.x
                >= self.body.position.x - self.body.width
            )
            is_in_vertical = (
                self.body.position.y + self.body.height
                >= other.body.position.y
                >= self.body.position.y - self.body.height
            )

            return is_in_horizontal and is_in_vertical


class point_collider(collider):
    def __init__(self, body: Body.body) -> None:
        super().__init__(body)

    def collided(self, other: "collider") -> bool:
        if isinstance(other, point_collider):
            return False  # TODO can be done in later stages
        if isinstance(other, rect_collider):
            return other.collided(self)


class soft_body_collider(collider):
    def __init__(self, body: Body.soft_body | Body.body) -> None:
        super().__init__(body)
        self.body_colliders = []

        for v in self.body.vertecies:
            if not isinstance(v.collider, point_collider):
                v.collider = point_collider(v)
            self.body_colliders.append(v.collider)

    def collided(self, other: "collider") -> tuple[bool, list[point_collider]]:
        result = (False, list())
        if isinstance(other, rect_collider):
            for coll in self.body_colliders:
                breakpoint
                if not other.collided(coll):
                    continue
                result[1].append(coll)
                if not result[0]:
                    result = (True, result[1])
        if isinstance(other, point_collider):
            pass  # TODO Later stages
        if isinstance(other, soft_body_collider):
            pass  # TODO Later stages
        return result
