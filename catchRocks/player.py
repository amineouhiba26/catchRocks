import pygame


class Player:
    playerNb = 0

    def __init__(self, dx=15, height=50) -> None:
        Player.playerNb += 1
        self.dx = dx

        if (Player.playerNb == 1):
            self.player = pygame.image.load(
                './assets/images/perso.png').convert_alpha()
        else:
            self.player = pygame.image.load(
                './assets/images/perso2.png').convert_alpha()
        # needs refining
        original_width, original_height = self.player.get_rect().size

        aspect_ratio = original_width / original_height

        self.scaled_width = int(height * aspect_ratio)

        self.player = pygame.transform.scale(
            self.player, (self.scaled_width, height))

        self.playerRect = self.player.get_rect()
        if (Player.playerNb == 1):
            self.playerRect.center = ((1280/2) - 50, 720-self.scaled_width/2)
        else:
            self.playerRect.center = ((1280/2) + 50, 720-self.scaled_width/2)

        self.score = 0
        self.name: str = ""

    def moveLeftPlayer(self):
        if (self.playerRect.left < 0):
            return
        self.playerRect.x -= self.dx

    def moveRightPlayer(self, width):
        if (self.playerRect.right > width):
            return
        self.playerRect.x += self.dx

    def detectCollision(self, targetRect):
        return self.playerRect.colliderect(targetRect)

    def drawPlayer(self, screen):
        screen.blit(self.player, self.playerRect)

    def resetPlayerPos(self):
        self.playerRect.center = (1280/2, 720-self.scaled_width/2)
