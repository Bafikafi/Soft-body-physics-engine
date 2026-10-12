import pygame


class rigid_object_rectangle:
    position = pygame.Vector2(0, 0)
    width = 0
    height = 0

    def __init__(self, position: pygame.Vector2, width: float, height: float) -> None:
        self.position = position
        self.width = width
        self.height = height

    def draw(self, display):
        pygame.draw.rect(
            display,
            (0, 0, 0),
            pygame.rect(self.position.x, self.position.y, self.width, self.height),
        )
