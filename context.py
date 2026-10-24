from __future__ import annotations
from attr import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import body as Body
    import collision_detection
    from pygame import Vector2



@dataclass
class contact:
    body: Body.body
    collision: collision_detection.collider
    normal: Vector2
    penetration: float

@dataclass
class physics_context:
    contacts: list[collision_detection.contact]