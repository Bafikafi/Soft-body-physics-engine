import pytest
import pygame

import physics
import consts


@pytest.fixture
def make_vertex():
    def create(vx=0, vy=0, springs=None):
        # Simple test double for the vertex interface.
        class TestVertex:
            pass

        vertex = TestVertex()
        vertex.velocity = pygame.Vector2(vx, vy)
        vertex.springs = springs if springs is not None else []
        return vertex

    return create


@pytest.fixture(autouse=True)
def friction_settings(monkeypatch):
    monkeypatch.setattr(physics, "GRAVITY_ACCELERATION", 20)
    monkeypatch.setattr(consts, "FRICTION_CONSTANT", 0.5, raising=False)
    monkeypatch.setattr(consts, "DELTA", 0.1)


@pytest.mark.parametrize("vx", [10, -10])
def test_friction_slows_horizontal_motion(make_vertex, vx):
    vertex = make_vertex(vx=vx)
    normal = pygame.Vector2(0, -1)

    physics.apply_friction(vertex, normal)

    assert abs(vertex.velocity.x) < abs(vx)
    assert vertex.velocity.x * vx >= 0
    assert vertex.velocity.y == pytest.approx(0)


def test_friction_does_not_reverse_velocity(make_vertex):
    vertex = make_vertex(vx=0.01)

    physics.apply_friction(vertex, pygame.Vector2(0, -1))

    assert vertex.velocity.x == pytest.approx(0)


def test_stationary_vertex_remains_stationary(make_vertex):
    vertex = make_vertex()

    physics.apply_friction(vertex, pygame.Vector2(0, -1))

    assert vertex.velocity == pygame.Vector2(0, 0)


def test_no_normal_load_means_no_friction(make_vertex, monkeypatch):
    vertex = make_vertex(vx=10)

    monkeypatch.setattr(physics, "GRAVITY_ACCELERATION", 0)

    physics.apply_friction(vertex, pygame.Vector2(0, -1))

    assert vertex.velocity.x == pytest.approx(10)


def test_friction_against_vertical_wall(make_vertex, monkeypatch):
    vertex = make_vertex(vx=0, vy=10)

    monkeypatch.setattr(
        physics,
        "calculate_spring_force",
        lambda spring: pygame.Vector2(-20, 0),
        raising=False,
    )
    vertex.springs = [object()]

    physics.apply_friction(vertex, pygame.Vector2(1, 0))

    assert 0 <= vertex.velocity.y < 10
    assert vertex.velocity.x == pytest.approx(0)


def test_spring_load_increases_friction(make_vertex, monkeypatch):
    spring = object()

    monkeypatch.setattr(
        physics,
        "calculate_spring_force",
        lambda s: pygame.Vector2(0, 20),
        raising=False,
    )

    without_spring = make_vertex(vx=10)
    with_spring = make_vertex(vx=10, springs=[spring])

    normal = pygame.Vector2(0, -1)

    physics.apply_friction(without_spring, normal)
    physics.apply_friction(with_spring, normal)

    assert abs(with_spring.velocity.x) < abs(without_spring.velocity.x)


def test_friction_with_diagonal_normal(make_vertex, monkeypatch):
    vertex = make_vertex(vx=10, vy=0)

    monkeypatch.setattr(
        physics,
        "calculate_spring_force",
        lambda spring: pygame.Vector2(-20, 0),
        raising=False,
    )
    vertex.springs = [object()]

    normal = pygame.Vector2(1, -1).normalize()
    tangent = pygame.Vector2(-normal.y, normal.x)

    before = vertex.velocity.dot(tangent)

    physics.apply_friction(vertex, normal)

    after = vertex.velocity.dot(tangent)

    assert abs(after) < abs(before)
    assert before * after >= 0
