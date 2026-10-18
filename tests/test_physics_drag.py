import pytest
import pygame

import physics
import consts


@pytest.fixture
def make_vertex():
    def create(vx=0, vy=0):
        vertex = type("TestVertex", (), {})()
        vertex.velocity = pygame.Vector2(vx, vy)
        return vertex

    return create


@pytest.fixture(autouse=True)
def drag_settings(monkeypatch):
    monkeypatch.setattr(consts, "DRAG_COEFFICIENT", 2.0)
    monkeypatch.setattr(consts, "DELTA", 0.1)


@pytest.mark.parametrize(
    "vx, vy",
    [
        (10, 0),
        (-10, 0),
        (0, 10),
        (0, -10),
        (10, -20),
    ],
)
def test_drag_reduces_velocity(make_vertex, vx, vy):
    vertex = make_vertex(vx, vy)
    original_speed = vertex.velocity.length()

    physics.apply_drag(vertex)

    assert vertex.velocity.length() < original_speed


def test_drag_calculates_correct_velocity(make_vertex):
    vertex = make_vertex(10, -20)

    physics.apply_drag(vertex)

    # v_new = v_old * (1 - coefficient * dt)
    assert vertex.velocity.x == pytest.approx(8)
    assert vertex.velocity.y == pytest.approx(-16)


def test_stationary_vertex_remains_stationary(make_vertex):
    vertex = make_vertex()

    physics.apply_drag(vertex)

    assert vertex.velocity == pygame.Vector2(0, 0)


def test_zero_drag_coefficient(make_vertex, monkeypatch):
    monkeypatch.setattr(consts, "DRAG_COEFFICIENT", 0)

    vertex = make_vertex(10, -5)

    physics.apply_drag(vertex)

    assert vertex.velocity == pygame.Vector2(10, -5)


def test_zero_delta_time(make_vertex, monkeypatch):
    monkeypatch.setattr(consts, "DELTA", 0)

    vertex = make_vertex(10, -5)

    physics.apply_drag(vertex)

    assert vertex.velocity == pygame.Vector2(10, -5)


def test_stronger_drag_causes_more_deceleration(make_vertex, monkeypatch):
    weak = make_vertex(10, 0)
    strong = make_vertex(10, 0)

    monkeypatch.setattr(consts, "DRAG_COEFFICIENT", 1.0)
    physics.apply_drag(weak)

    monkeypatch.setattr(consts, "DRAG_COEFFICIENT", 4.0)
    physics.apply_drag(strong)

    assert strong.velocity.length() < weak.velocity.length()


def test_drag_does_not_change_direction(make_vertex):
    vertex = make_vertex(10, -20)
    original = vertex.velocity.copy()

    physics.apply_drag(vertex)

    assert vertex.velocity.dot(original) > 0


def test_drag_never_increases_speed(make_vertex):
    vertex = make_vertex(10, 0)

    physics.apply_drag(vertex)

    assert vertex.velocity.length() <= 10
