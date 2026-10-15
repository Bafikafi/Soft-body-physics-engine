import pytest
import collision_detection
from unittest.mock import Mock, patch
from pygame import Vector2
from contextlib import ExitStack


def test_point_collider():
    body = Mock()
    body.position = Vector2(5, 5)
    body.velocity = Vector2(0, 0)

    collider = collision_detection.point_collider(body)
    assert collider.body.position == Vector2(5, 5)


@pytest.mark.parametrize(
    "x, y, result",
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
def test_point_in_rectangle(x, y, result):
    body_a = Mock()
    body_a.position = Vector2(x, y)
    body_b = Mock()
    body_b.position = Vector2(5, 5)
    body_b.width = 5
    body_b.height = 5

    collider_a = collision_detection.point_collider(body_a)
    collider_b = collision_detection.rect_collider(body_b)

    assert (
        collider_a.collided(collider_b)[0] == result
        and collider_b.collided(collider_a)[0] == result
    )


def make_point(x, y):
    body = Mock()
    body.position = Vector2(x, y)
    return collision_detection.point_collider(body)


def test_soft_body_collider():
    positions = [Vector2(5, 5), Vector2(10, 10), Vector2(15, 15)]
    body_a = Mock()
    body_a.vertecies = []
    for pos in positions:
        body_a.vertecies.append(Mock(position=pos))
    collider_a = collision_detection.soft_body_collider(body_a)
    test_pos = []
    for i in collider_a.body.vertecies:
        test_pos.append(i.position)
    assert positions == test_pos


@pytest.mark.parametrize(
    "positions, x, y, width, height, result",
    [
        (
            [Vector2(5, 5), Vector2(7, 7), Vector2(15, 15)],
            5,
            5,
            5,
            5,
            (True, [make_point(5, 5), make_point(7, 7)]),
        )
    ],
)
def test_soft_body_rect_collisions(
    positions: list(Vector2()), x, y, width, height, result
):
    body_a = Mock()
    body_a.vertecies = []
    for pos in positions:
        body_a.vertecies.append(Mock(position=pos))
    collider_a = collision_detection.soft_body_collider(body_a)

    body_b = Mock()
    body_b.position, body_b.width, body_b.height = Vector2(x, y), width, height
    collider_b = collision_detection.rect_collider(body_b)
    res = collider_a.collided(collider_b)
    eq_points = True
    for i in result[1]:
        for j in res[1]:
            if (
                j.body.position.x == i.body.position.x
                and j.body.position.y == i.body.position.y
            ):
                eq_points = True
                break
            eq_points = False
        if not eq_points:
            break

    assert res[0] == result[0] and eq_points == True


@pytest.mark.parametrize(
    "positions, x, y, width, length", [[Vector2(5, 5), Vector2(20, 20)], 5, 7, 6, 6]
)
def detector_call(positions, x, y, width, length):
    detector = collision_detection.collision_detector()
    soft_body = Mock(vertecies=[])
    body_b = Mock()
    body_b.position, body_b.width, body_b.height = Vector2(x, y), width, length
    collider_b = collision_detection.rect_collider(body_b, detector)
    for i in positions:
        soft_body.vertecies.append(Mock(position=i))
    soft_body_col = collision_detection.soft_body_collider(soft_body, detector)
    with ExitStack() as stack:
        mocks = [
            stack.enter_context(patch.object(point, "response"))
            for point in soft_body_col.body_colliders
        ]
        detector.update()
        mocks[0].assert_called_once()
        mocks[1].assert_not_called()


import pytest
import pygame
from unittest.mock import Mock

import body as Body
from collision_detection import point_collider, rect_collider


@pytest.mark.parametrize(
    "position, velocity, expected_position, expected_velocity",
    [
        # From above
        ((0, -4), (3, 5), (0, -5), (3, 0)),
        # From below
        ((0, 4), (3, -5), (0, 5), (3, 0)),
        # From left
        ((-9, 0), (5, 3), (-10, 0), (0, 3)),
        # From right
        ((9, 0), (-5, 3), (10, 0), (0, 3)),
        # Moving away from the surface
        ((0, -4), (3, -5), (0, -5), (3, -5)),
        # Sliding along the surface
        ((0, -4), (5, 0), (0, -5), (5, 0)),
    ],
)
def test_point_collider_response(
    position,
    velocity,
    expected_position,
    expected_velocity,
):
    point_body = Mock()
    point_body.position = pygame.Vector2(position)
    point_body.velocity = pygame.Vector2(velocity)

    rect_body = Mock(spec=Body.rigid_object_rectangle)
    rect_body.position = pygame.Vector2(0, 0)
    rect_body.width = 20
    rect_body.height = 10

    point = point_collider(point_body)
    rectangle = rect_collider(rect_body)

    point.response(rectangle)

    assert point_body.position == pygame.Vector2(expected_position)
    assert point_body.velocity == pygame.Vector2(expected_velocity)
