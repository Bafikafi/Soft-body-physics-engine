import pytest
import pygame
from unittest.mock import Mock, patch

import body as Body
import collision_detection as collision
import physics


@pytest.fixture
def make_point():
    def create(x, y, vx=0, vy=0):
        point_body = Mock()
        point_body.position = pygame.Vector2(x, y)
        point_body.velocity = pygame.Vector2(vx, vy)
        point_body.springs = []
        point_body.collider = None
        return collision.point_collider(point_body)

    return create


@pytest.fixture
def make_rectangle():
    def create(x=5, y=5, width=5, height=5):
        rect_body = Body.rigid_object_rectangle(x, y, width, height)
        return collision.rect_collider(rect_body)

    return create


@pytest.fixture
def make_soft_body():
    def create(positions):
        soft_body = Body.soft_body()
        for x, y in positions:
            vertex = Mock()
            vertex.position = pygame.Vector2(x, y)
            vertex.velocity = pygame.Vector2(0, 0)
            vertex.springs = []
            vertex.collider = None
            soft_body.vertecies.append(vertex)
        return collision.soft_body_collider(soft_body)

    return create


def test_point_collider_stores_body(make_point):
    point = make_point(5, 5)
    assert point.body.position == pygame.Vector2(5, 5)


@pytest.mark.parametrize(
    'x, y, expected',
    [
        (5, 5, True),
        (7, 7, True),
        (10, 5, False),
        (5, 10, False),
        (10, 10, False),
        (11, 5, False),
        (5, 11, False),
        (11, 11, False),
        (100, 100, False),
        (-10, 5, False),
        (5, -10, False),
        (-10, -10, False),
    ],
)
def test_point_rectangle_collision(make_point, make_rectangle, x, y, expected):
    point = make_point(x, y)
    rectangle = make_rectangle()
    assert point.collided(rectangle)[0] is expected
    assert rectangle.collided(point)[0] is expected


def test_soft_body_collider_registers_point_colliders(make_soft_body):
    positions = [(5, 5), (10, 10), (15, 15)]
    soft = make_soft_body(positions)
    assert len(soft.body_colliders) == len(positions)
    assert all(isinstance(c, collision.point_collider) for c in soft.body_colliders)
    assert [c.body.position for c in soft.body_colliders] == [
        pygame.Vector2(p) for p in positions
    ]


def test_soft_body_collider_reuses_existing_point_colliders():
    soft_body = Body.soft_body()
    vertex = Mock()
    vertex.position = pygame.Vector2(5, 5)
    vertex.velocity = pygame.Vector2(0, 0)
    vertex.springs = []
    existing = collision.point_collider(vertex)
    vertex.collider = existing
    soft_body.vertecies.append(vertex)

    soft = collision.soft_body_collider(soft_body)
    assert soft.body_colliders == [existing]


@pytest.mark.parametrize(
    'positions, expected_hits',
    [
        ([(5, 5), (7, 7), (15, 15)], [(5, 5), (7, 7)]),
        ([(15, 15), (20, 20)], []),
        ([(5, 5), (5, 5), (15, 15)], [(5, 5), (5, 5)]),
    ],
)
def test_soft_body_rectangle_collisions(
    make_soft_body, make_rectangle, positions, expected_hits
):
    soft = make_soft_body(positions)
    rectangle = make_rectangle()
    result = soft.collided(rectangle)

    assert result[0] is bool(expected_hits)
    actual_hits = [tuple(c.body.position) for c in result[1]]
    assert actual_hits == expected_hits
    if expected_hits:
        assert result[2] is rectangle


def test_detector_calls_response_only_for_colliding_point(
    make_soft_body, make_rectangle
):
    detector = collision.collision_detector()
    rectangle = make_rectangle(x=5, y=7, width=6, height=6)
    soft = make_soft_body([(5, 5), (20, 20)])
    detector.add_collider(rectangle)
    detector.add_collider(soft)

    with (
        patch.object(soft.body_colliders[0], 'response') as hit_response,
        patch.object(soft.body_colliders[1], 'response') as miss_response,
    ):
        detector.update()
        hit_response.assert_called_once_with(rectangle)
        miss_response.assert_not_called()


@pytest.mark.parametrize(
    'position, velocity, expected_position, expected_velocity',
    [
        ((0, -4), (3, 5), (0, -5), (3, 0)),
        ((0, 4), (3, -5), (0, 5), (3, 0)),
        ((-9, 0), (5, 3), (-10, 0), (0, 3)),
        ((9, 0), (-5, 3), (10, 0), (0, 3)),
        ((0, -4), (3, -5), (0, -5), (3, -5)),
        ((0, -4), (5, 0), (0, -5), (5, 0)),
    ],
)
def test_point_collider_response_without_friction(
    make_point, monkeypatch, position, velocity, expected_position, expected_velocity
):
    # Friction has separate unit tests; isolate penetration and normal velocity.
    monkeypatch.setattr(physics, 'apply_friction', lambda *args, **kwargs: None, raising=False)

    point = make_point(*position, *velocity)
    rectangle_body = Body.rigid_object_rectangle(0, 0, 20, 10)
    rectangle = collision.rect_collider(rectangle_body)

    point.response(rectangle)

    assert point.body.position == pygame.Vector2(expected_position)
    assert point.body.velocity == pygame.Vector2(expected_velocity)
