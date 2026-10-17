import json
from unittest.mock import Mock, patch

import pytest

import softbody_factory as builder


@pytest.fixture
def softbody_data():
    return {
        "vertecies": [
            {"id": 0, "x": 0, "y": 0},
            {"id": 1, "x": 3, "y": 4},
            {"id": 2, "x": 6, "y": 0},
        ],
        "springs": [
            {"from": 0, "to": 1},
            {"from": 1, "to": 2},
        ],
        "stiffness": 100,
    }


@pytest.fixture
def json_file(tmp_path, softbody_data):
    path = tmp_path / "softbody.json"
    path.write_text(json.dumps(softbody_data), encoding="utf-8")
    return str(path)


def test_json_parse(json_file, softbody_data):
    assert builder._json_parse(json_file) == softbody_data


def test_create_vertices(softbody_data):
    vertices = builder._create_vertecies(softbody_data["vertecies"])

    assert len(vertices) == 3
    assert set(vertices.keys()) == {0, 1, 2}

    assert vertices[0].position.x == 0
    assert vertices[0].position.y == 0

    assert vertices[1].position.x == 3
    assert vertices[1].position.y == 4


def test_create_springs(softbody_data):
    vertices = builder._create_vertecies(softbody_data["vertecies"])

    springs = builder._create_springs(
        softbody_data["springs"],
        vertices,
        stiffness=100,
    )

    assert len(springs) == 2


def test_add_colliders(softbody_data):
    vertices = builder._create_vertecies(
        softbody_data["vertecies"]
    )

    softbody = builder._create_softbody(
        vertices.values(), []
    )

    detector = Mock()

    builder._add_colliders(
        softbody,
        vertices.values(),
        detector,
    )

    for vertex in vertices.values():
        assert vertex.collider is not None

    detector.add_collider.assert_called_once()

    registered_collider = detector.add_collider.call_args.args[0]

    assert isinstance(
        registered_collider,
        builder.collision_detection.soft_body_collider
    )
    assert registered_collider.body is softbody


def test_build(json_file):
    detector = Mock()

    softbody = builder.build(json_file, detector)

    assert softbody is not None
    assert len(softbody.vertecies) == 3
