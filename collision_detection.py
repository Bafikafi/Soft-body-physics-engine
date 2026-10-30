from __future__ import annotations
from math import copysign
import pygame
from abc import ABC, abstractmethod
import body as Body
import physics
from context import contact
from dataclasses import dataclass, replace


@dataclass
class detection_response:
    detected: bool
    source: "collider"
    components: None | list["collider"]
    target: "collider"


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

                result = self.colliders[i].detect(self.colliders[j])
                if not result.detected:
                    continue
                reversed_result = replace(result, source=result.target, target = result.source)
                self.colliders[i].response(result)
                self.colliders[j].response(reversed_result)


class collider(ABC):
    def __init__(
        self, body: Body.body, collision_detector: collision_detector = None
    ) -> None:
        self.body = body
        if collision_detector != None:
            collision_detector.add_collider(self)

    # TODO Refactor - wtf tuple, use dataclass
    # *Done ^‿^
    @abstractmethod
    def detect(self, other: "collider") -> detection_response:
        pass

    @abstractmethod
    def response(self, result: detection_response) -> None:
        pass


class rect_collider(collider):
    def _detect_point(self, other: "collider") -> bool:
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
        return is_in_horizontal and is_in_vertical

    def _detect_soft_body(
        self, other: "collider"
    ) -> detection_response:
        return other.detect(self)

    def detect(self, other: "collider") -> detection_response:
        detected = False
        components = None

        if isinstance(other, rect_collider):
            raise NotImplementedError("Rect collision not implemented")

        elif isinstance(other, point_collider):
            detected = self._detect_point(other)

        elif isinstance(other, soft_body_collider):
            res = self._detect_soft_body(other)
            detected = res.detected
            components = res.components

        else:
            raise NotImplementedError("Collider type not supported")

        return detection_response(
            detected=detected,
            source=self,
            target=other,
            components=components
        )

    def response(self, result: detection_response) -> None:
        return super().response(result)  # *No functionality needed for prototype


class point_collider(collider):
    def detect(self, other: "collider") -> detection_response:
        if isinstance(other, point_collider):
            raise NotImplementedError(
                "Feature is not implemented"
            )  # TODO can be done in later stages
        if isinstance(other, rect_collider):
            res = other.detect(self)
            res.source, res.target = res.target, res.source
            return res

    """
    TODO Refactor - have collision predicted, respond based off prediction
    Should create smoother collisions 
    """

    def _response_rect_collider(self, other: "collider"):
        rect_body = other.body
        diff = self.body.position - rect_body.position
        dl = rect_body.height / 2 - abs(diff.y)
        dw = rect_body.width / 2 - abs(diff.x)
        penetration = pygame.Vector2(0, 0)
        if dl < dw:
            norm = pygame.Vector2(0, copysign(1, diff.y))
            penetration.y = copysign(dl, diff.y)
        else:
            norm = pygame.Vector2(copysign(1, diff.x), 0)
            penetration.x = copysign(dw, diff.x)
        #            self.body.velocity = (
        #          self.body.velocity
        #           - min(0, pygame.Vector2.dot(self.body.velocity, norm)) * norm
        #        )
        return contact(collision=other, normal=norm, penetration=0)

    def response(self, result: detection_response) -> None:
        # !Rectangle class have no rotation
        if not isinstance(result.target.body, Body.rigid_object_rectangle):
            raise NotImplementedError(
                "Feature not implemented - can't collide with points"
            )
        self.body.context.contacts.append(self._response_rect_collider(result.target))


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

    def detect(self, other: "collider") -> detection_response:
        result = detection_response(
            detected=False, source=self, components=list(), target=other
        )
        if isinstance(other, rect_collider):
            for coll in self.body_colliders:
                if not other.detect(coll).detected:
                    continue
                result.components.append(coll)
                if not result.detected:
                    result.detected = True
        if isinstance(other, point_collider):
            raise NotImplementedError("Feature not implemented")
        if isinstance(other, soft_body_collider):
            raise NotImplementedError("Feature not implemented")
        return result

    def response(self, result: detection_response) -> None:
        if not result.components:
            return
        for coll in result.components:
            coll.response(result)
