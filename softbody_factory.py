import json
import body as Body
import collision_detection
from typing import Any


def _json_parse(file_path: str) -> dict[str, Any]:
    with open(file_path) as file:
        data = file.read()
    return json.loads(data)


def _create_vertecies(vertecies_ids: list[dict[str, int]]) -> dict[int, Body.vertex]:
    vertecies = dict()
    for vertex_id in vertecies_ids:
        vertecies[vertex_id["id"]] = Body.vertex(vertex_id["x"], vertex_id["y"])
    return vertecies


def _add_colliders(
    body: Body.soft_body,
    vertecies: list[Body.vertex],
    detector: collision_detection.collision_detector,
) -> None:
    for vertex in vertecies:
        vertex.add_point_collider(collision_detection.point_collider(vertex))
    detector.add_collider(collision_detection.soft_body_collider(body))


def _create_springs(
    spring_ids: list[dict[str, int]],
    vertecies_ids: dict[int, Body.vertex],
    stiffness: float,
) -> list[Body.spring_edge]:
    springs = list()
    for spring_id in spring_ids:
        vertex_a = vertecies_ids[spring_id["from"]]
        vertex_b = vertecies_ids[spring_id["to"]]
        length = (vertex_b.position - vertex_a.position).length()
        spring = Body.spring_edge(vertex_a, vertex_b, length, stiffness)
        vertex_a.springs.append(spring)
        vertex_b.springs.append(spring)
        springs.append(spring)
    return springs


def _create_softbody(
    vertecies: list[Body.vertex], springs: list[Body.spring_edge]
) -> Body.soft_body:
    softbody = Body.soft_body()
    for vertex in vertecies:
        softbody.add_vertex(vertex)
    for spring in springs:
        softbody.add_spring(spring)
    return softbody


def build(
    file_path: str, detector: collision_detection.collision_detector
) -> Body.soft_body:
    data = _json_parse(file_path)
    vertex_ids = _create_vertecies(data["vertecies"])
    springs = _create_springs(data["springs"], vertex_ids, data["stiffness"])
    softbody = _create_softbody(vertex_ids.values(), springs)
    _add_colliders(softbody, vertex_ids.values(), detector)
    return softbody
