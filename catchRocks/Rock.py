import pygame
from constValue import rockVel


class Rock:
    def __init__(self, x, y, width, height):
        self.vel = rockVel
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rockImg = pygame.image.load(
            "assets/images/rockImg.png").convert_alpha()
        self.rockImg = pygame.transform.scale(
            self.rockImg, (self.width, self.height))
        self.rockRect = self.rockImg.get_rect()

        self.rockRect.center = (self.x, (-height)//2)

    def Fall(self):
        self.y += self.vel
        self.rockRect.y += self.vel

    def draw(self, screen):
        self.rockRect.x = self.x
        screen.blit(self.rockImg, self.rockRect)
