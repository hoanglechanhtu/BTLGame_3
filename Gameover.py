import pygame
from params import *

game_over_scr = pygame.transform.scale(pygame.image.load('asset/Environment/background/game_over.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))

class GameOver:
    _instance = None

    @staticmethod
    def getInstance():
        if GameOver._instance == None:
            GameOver()
        return GameOver._instance


    def __init__(self):
        if GameOver._instance != None:
            raise Exception("This class is a singleton!")
        else:
            GameOver._instance = self
            self.lives = 3


    def is_game_over(self):
        return self.lives <= 0

    def reduce_life(self):
        print("Lives" + str(self.lives))
        self.lives = self.lives - 1

    def reset(self):
        self.lives = 3

    def draw(self, window, msg_Y):
        window.blit(game_over_scr, (0,0))

        font = pygame.font.Font(None, 80)
        msg = pygame.Surface((GAME_OVER_TEXT_WIDTH, GAME_OVER_TEXT_HEIGHT), pygame.SRCALPHA, 32)
        msg = msg.convert_alpha()

        text = font.render('Press Enter to return', True, (255, 255, 255))
        msg.blit(text, (MENU_OPTIONS_WIDTH // 2 - text.get_width() // 2,
                         MENU_OPTIONS_HEIGHT // 2 - text.get_height() // 2))


        window.blit(msg, (SCREEN_WIDTH // 2 - GAME_OVER_TEXT_WIDTH // 2, msg_Y))