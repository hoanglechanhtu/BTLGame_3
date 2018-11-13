import pygame
from params import *

game_over_scr = pygame.transform.scale(pygame.image.load('asset/Environment/background/game_over.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
mission_clear_scr = pygame.transform.scale(pygame.image.load('asset/Environment/background/mission_clear.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
class GameState:
    _instance = None

    @staticmethod
    def getInstance():
        if GameState._instance == None:
            GameState()
        return GameState._instance


    def __init__(self):
        if GameState._instance != None:
            raise Exception("This class is a singleton!")
        else:
            GameState._instance = self
            self.lives = 10
            self.is_won = False


    def is_game_over(self):
        return self.lives <= 0

    def is_game_won(self):
        return self.is_won;

    def reduce_life(self):
        print("Lives" + str(self.lives))
        self.lives = self.lives - 1

    def reset(self):
        self.lives = 10
        self.is_won = False

    def on_boss_death(self):
        self.is_won = True

    def draw_game_over(self, window, msg_Y):
        window.blit(game_over_scr, (0,0))

        font = pygame.font.Font(None, 80)
        msg = pygame.Surface((GAME_OVER_TEXT_WIDTH, GAME_OVER_TEXT_HEIGHT), pygame.SRCALPHA, 32)
        msg = msg.convert_alpha()

        text = font.render('Press Space to return', True, (255, 255, 255))
        msg.blit(text, (GAME_OVER_TEXT_WIDTH // 2 - text.get_width() // 2,
                        GAME_OVER_TEXT_HEIGHT // 2 - text.get_height() // 2))


        window.blit(msg, (SCREEN_WIDTH // 2 - GAME_OVER_TEXT_WIDTH // 2, msg_Y))

    def draw_game_win(self, window, msg_Y):
        window.blit(mission_clear_scr, (0,0))

        font = pygame.font.Font(None, 80)
        msg = pygame.Surface((GAME_WIN_TEXT_WIDTH, GAME_WIN_TEXT_HEIGHT), pygame.SRCALPHA, 32)
        msg = msg.convert_alpha()

        text = font.render('Press Space to return', True, (255, 255, 255))
        msg.blit(text, (GAME_WIN_TEXT_WIDTH // 2 - text.get_width() // 2,
                        GAME_WIN_TEXT_HEIGHT // 2 - text.get_height() // 2))


        window.blit(msg, (SCREEN_WIDTH // 2 - GAME_WIN_TEXT_WIDTH // 2, msg_Y))