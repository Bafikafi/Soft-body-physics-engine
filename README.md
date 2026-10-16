# SoftBody Physics Engine
An experimental 2D mass-spring physics engine written in Python using Pygame.
Originally created for two interactive anti-stress toys as part of CodeWeek.
Somehow evolved into a physics engine.

**Current state**:
- supports one spring-mass soft-body
- capable of creating from json file Eg:
```json
{
    "name": "test",
    "stiffness": 1200,
    "vertecies": [
        {"id": 0, "x": 200, "y":150},
        {"id": 1, "x": 300, "y":150},
        {"id": 2, "x": 250, "y":200}
    ],
    "springs":[
        {"from": 0, "to": 1},
        {"from": 0, "to": 2},
        {"from": 1, "to": 2}
    ]
}
```
- support soft-body collisions with other rigidbody objects (currently non-rotating, one axis rectange)

*Note*: Still under development
