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
            (255, 255, 255),
            pygame.rect.Rect(
                rigid_body.position.x - rigid_body.width / 2,
                rigid_body.position.y - rigid_body.height / 2,
                rigid_body.width,
                rigid_body.height,
            ),
        )
