import pygame


class renderer:
    @staticmethod
    def render_debug(display: pygame.display, objs):
        if type(objs) != list:
            objs = [objs]

        for obj in objs:
            pygame.draw.circle(
                display, color=(255, 0, 0), center=obj.position, radius=5
            )

    @staticmethod
    def redner_edge_debug(display: pygame.display, objs):
        if type(objs) != list:
            objs = [objs]
        for obj in objs:
            pygame.draw.line(
                display, (0, 255, 0), obj.vertex_a.position, obj.vertex_b.position
            )

    @staticmethod
    def render_rigid_object(display: pygame.display, rigid_body):
        pygame.draw.rect(
            display,
            (0, 0, 0),
            pygame.rect(
                rigid_body.position.x,
                rigid_body.position.y,
                rigid_body.width,
                rigid_body.height,
            ),
        )
