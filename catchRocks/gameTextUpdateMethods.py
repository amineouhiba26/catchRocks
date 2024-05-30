import pygame
from player import Player
from Rock import Rock
from constValue import *


class gameTextUpdateMethods:
    @staticmethod
    def draw_restart_prompt(screen: pygame.Surface):
        font = pygame.font.Font(None, 50)
        # QUIT
        quit_prompt_text = font.render(
            " Escape to quit", True, (0, 0, 0))
        quit_prompt_text_rect = quit_prompt_text.get_rect()
        quit_prompt_text_rect.center = (
            screenWidth // 2, (screenHeight // 2)+100)
        screen.blit(quit_prompt_text, quit_prompt_text_rect)

        restart_prompt_text = font.render("R to restart", True, (0, 0, 0))
        restart_prompt_text_rect = restart_prompt_text.get_rect()
        restart_prompt_text_rect.center = (
            screenWidth // 2, (screenHeight // 2)+50)

        screen.blit(restart_prompt_text, restart_prompt_text_rect)

    @staticmethod
    def updatePlayer1Score(font: pygame.font.Font, screen: pygame.Surface, score, text):
        score_text = font.render(f'{text}: {score}', True, (0, 0, 0))
        scoreRect = score_text.get_rect()
        scoreRect.top = 25
        scoreRect.left = 50
        screen.blit(score_text, scoreRect)

    @staticmethod
    def updatePlayer2Score(font: pygame.font.Font, screen: pygame.Surface, score, text):
        score_text = font.render(f'{text}: {score}', True, (0, 0, 0))
        scoreRect = score_text.get_rect()
        scoreRect.top = 25
        scoreRect.right = screenWidth-50
        screen.blit(score_text, scoreRect)

    @staticmethod
    def draw_winner(screen, winner_name):
        font = pygame.font.Font(None, 50)
        winner_text = font.render(
            f"{winner_name} wins!", True, (0, 0, 0))
        winner_text_rect = winner_text.get_rect()
        winner_text_rect.center = (screenWidth //
                                   2, (screenHeight // 2) - 25)
        screen.blit(winner_text, winner_text_rect)

    @staticmethod
    def draw_paused(screen: pygame.Surface):
        font = pygame.font.Font(None, 60)

        # QUIT
        quit_prompt_text = font.render(
            "Game is paused! ,press o to unpause", True, (0, 0, 0))
        quit_prompt_text_rect = quit_prompt_text.get_rect()
        quit_prompt_text_rect.center = (
            screenWidth // 2, (screenHeight // 2))
        screen.blit(quit_prompt_text, quit_prompt_text_rect)
