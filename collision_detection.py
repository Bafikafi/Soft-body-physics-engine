from __future__ import annotations
from math import copysign
import pygame
from abc import ABC, abstractmethod
import body as Body
import physics


class collision_detector:
    def __init__(self, colliders: list("collider") | None = None) -> None:
        self.colliders = [] if colliders is None else colliders

    def add_collider(self, collider: "collider"):
        self.colliders.append(collider)

    """
    TODO Refactor - not calling response based on if soft-body or not
     (use response of sof)
    """

    def update(self):
        for i in range(len(self.colliders)):
            for j in range(i, len(self.colliders)):
                if i == j:
                    continue

                if isinstance(self.colliders[j], soft_body_collider):
                    result = self.colliders[j].collided(self.colliders[i])
                    other = self.colliders[i]
                else:
                    result = self.colliders[i].collided(self.colliders[j])
                    other = self.colliders[j]
                if not result[0]:
                    continue
                for col in result[1]:
                    col.response(result[2])
                result[2].response(other)


class collider(ABC):
    def __init__(
        self, body: Body.body, collision_detector: collision_detector = None
    ) -> None:
        self.body = body
        if collision_detector != None:
            collision_detector.add_collider(self)

    # TODO Refactor - wtf tuple, use dataclass
    @abstractmethod
    def collided(self, other: "collider") -> tuple[bool, list["collider"], "collider"]:
        pass

    @abstractmethod
    def response(self, other: "collider") -> None:
        pass


class rect_collider(collider):
    def collided(self, other: "collider") -> tuple[bool, list["collider"], "collider"]:
        if isinstance(other, rect_collider):
            if not isinstance(other.body, Body.rigid_object_rectangle):
                raise NotImplementedError("Feature is not implemented")
                # !fix later, not needed for product
        if isinstance(other, point_collider):
            is_in_horizontal = (
                self.body.position.x + self.body.width / 2
                >= other.body.position.x
                >= self.body.position.x - self.body.width / 2
            )
            is_in_vertical = (
                self.body.position.y + self.body.height / 2
                >= other.body.position.y
                >= self.body.position.y - self.body.height / 2
            )

            return (is_in_horizontal and is_in_vertical, [self], other)

    def response(self, other: "collider") -> None:
        return super().response(other)  # *No functionality needed for prototype


class point_collider(collider):
    def collided(self, other: "collider") -> tuple[bool, list["collider"], "collider"]:
        if isinstance(other, point_collider):
            raise NotImplementedError(
                "Feature is not implemented"
            )  # TODO can be done in later stages
        if isinstance(other, rect_collider):
            res = other.collided(self)
            return (res[0], res[1], [self])

    """
    TODO Refactor - have collision predicted, respond based off prediction
    Should create smoother collisions 
    """

    def response(self, other: "collider") -> None:
        # !Rectangle class have no rotation
        if not isinstance(other.body, Body.rigid_object_rectangle):
            raise NotImplementedError(
                "Feature not implemented - can't collide with points"
            )
        rect_body = other.body
        diff = self.body.position - rect_body.position
        dl = rect_body.height / 2 - abs(diff.y)
        dw = rect_body.width / 2 - abs(diff.x)
        if dl < dw:
            self.body.position.y += copysign(dl, diff.y)
            norm = pygame.Vector2(0, copysign(1, diff.y))
        else:
            self.body.position.x += copysign(dw, diff.x)
            norm = pygame.Vector2(copysign(1, diff.x), 0)
        self.body.velocity = (
            self.body.velocity
            - min(0, pygame.Vector2.dot(self.body.velocity, norm)) * norm
        )
        physics.apply_friction(self.body, -norm)


"""
TODO Refactor - keep the collided point_colliders and save them inside class. 
When response is called - call response of all collided point_colliders
"""


class soft_body_collider(collider):
    def __init__(
        self,
        body: Body.soft_body | Body.body,
        collision_detector: collision_detector = None,
    ) -> None:
        super().__init__(body, collision_detector)
        self.body_colliders = []

        for v in self.body.vertecies:
            if not isinstance(v.collider, point_collider):
                v.collider = point_collider(v)
            self.body_colliders.append(v.collider)

    def collided(self, other: "collider") -> tuple[bool, list["collider"], "collider"]:
        result = (False, list())
        if isinstance(other, rect_collider):
            for coll in self.body_colliders:
                if not other.collided(coll)[0]:
                    continue
                result[1].append(coll)
                if not result[0]:
                    result = (True, result[1], other)
        if isinstance(other, point_collider):
            pass  # TODO Later stages
        if isinstance(other, soft_body_collider):
            pass  # TODO Later stages
        return result

    def response(self, other: "collider") -> None:
        pass  # *No funcitionality, composite class - Refactor will fix
