from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from pygame import Vector2
import consts
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
        self.force_modules: list[force_module] = list()
        self.constraints_modules: list[constraint_module] = list()
        self.accumulator = accumulator(self.body)
        self.integrator = integrator(self.body)
    
    def add_force_module(self, module: force_module):
        self.force_modules.append(module)
    
    def add_constraint_module(self, module: constraint_module):
        self.constraints_modules.append(module)
    
    def update(self):
        for mod in self.force_modules:
            mod.apply_forces(self.accumulator)
        self.integrator.step(self.accumulator)
        self.accumulator.reset()

class accumulator():
    def __init__(self, body: Body.soft_body) -> None:
        self.body = body
        self.forces = {}
        # Initialise forces dictionary
        for vertex in self.body.vertecies:
            self.forces[vertex] = Vector2(0, 0)
        
    def add_force(self, vertex: Body.vertex, force: Vector2):
        if vertex not in self.forces:
            self.forces[vertex] = Vector2(0, 0)
        self.forces[vertex] += force
    
    def add_vertex(self, vertex):
        if vertex in self.forces.keys():
            return
        self.forces[vertex] = Vector2(0, 0)
    
    def remove_vertex(self, vertex):
        self.forces.pop(vertex, None)

    def reset(self):
        for force in self.forces.values():
            force.update(0, 0)
    
    def get_forces(self) -> dict[Body.vertex, Vector2]:
        return self.forces
    
class integrator():
    def __init__(self, body: Body.soft_body) -> None:
        self.body = body   
    
    def step(self, accumulator: accumulator):
        forces = accumulator.get_forces()
        for vertex, force in forces.items():
            vertex.velocity += (force / vertex.mass) * consts.DELTA
            vertex.position += vertex.velocity * consts.DELTA
        

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


