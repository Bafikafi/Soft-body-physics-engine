from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from pygame import Vector2

if TYPE_CHECKING:
    import body as Body

class physics_module(ABC):
    
    def __init__(self, body: Body.soft_body) -> None:
        super().__init__()
        self.body = body


class force_module(physics_module):
    
    @abstractmethod
    def apply_forces(self, accumulator: accumulator) -> None:
        pass

class constraint_module(physics_module):
    @abstractmethod
    def solve(self):
        pass

class physics_system():
    def __init__(self, body: Body.soft_body) -> None:
        self.body = body

class accumulator():
    def __init__(self, body: Body.soft_body) -> None:
        self.body = body
        self.forces = {}
        # Do initialise forces dictionary
    def add_force(self, vertex: Body.vertex, force: Vector2):
        pass

class integrator():
    def __init__(self, body: Body.soft_body) -> None:
        self.body = body   
    

class gravity_force_module(force_module):
    def apply_forces(self, accumulator: accumulator) -> None:
        pass

class spring_force_module(force_module):
    def apply_forces(self, accumulator: accumulator) -> None:
        pass

class linear_drag_force_module(force_module):
    def apply_forces(self, accumulator: accumulator) -> None:
        pass

class friction_force_module(force_module):
    def apply_forces(self, accumulator: accumulator) -> None:
        pass


