from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import body as Body
    import collision_detection
    from pygame import Vector2



@dataclass
class contact:
    collision: collision_detection.collider
    normal: Vector2
    penetration: Vector2

@dataclass
class physics_context:
    contacts: list[collision_detection.contact]