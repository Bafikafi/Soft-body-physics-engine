import pytest
import collision_detection
from unittest.mock import Mock
from pygame import Vector2


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
        (10, 5, True),
        (5, 10, True),
        (10, 10, True),
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
        collider_a.collided(collider_b) == result
        and collider_b.collided(collider_a) == result
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
            [Vector2(5, 5), Vector2(10, 10), Vector2(15, 15)],
            5,
            5,
            5,
            5,
            (True, [make_point(5, 5), make_point(10, 10)]),
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
