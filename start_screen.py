import pygame
from params import *

start_scr_bg = pygame.transform.scale(pygame.image.load('asset/Environment/background/start_scr_bg.jpeg'),(SCREEN_WIDTH, SCREEN_HEIGHT))


class StartMenu:
    def __init__(self):
        self.options = []
        self.background = start_scr_bg
        self.chosen_option = 0

        self.load_options()

    def load_options(self):
        self.options.append('Start')
        self.options.append('Options')
        self.options.append('Exit')

    def change_option(self, is_down):
        if is_down:
            self.chosen_option = self.chosen_option + 1
            if (self.chosen_option > len(self.options) - 1):
                self.chosen_option = len(self.options) - 1
        else:
            self.chosen_option = self.chosen_option - 1
            if (self.chosen_option < 0):
                self.chosen_option = 0

    def draw(self, window, menu_Y):
        window.blit(start_scr_bg, (0, 0))

        font = pygame.font.Font(None, 80)
        menu = pygame.Surface((MENU_OPTIONS_WIDTH, MENU_OPTIONS_HEIGHT), pygame.SRCALPHA, 32)
        menu = menu.convert_alpha()
        for option in range(0, len(self.options)):
            if option == self.chosen_option:
                text = font.render(self.options[option], True, (255, 0, 0))
            else:
                text = font.render(self.options[option], True, (255, 255, 255))

            menu.blit(text, (MENU_OPTIONS_WIDTH // 2 - text.get_width() // 2,
                             MENU_OPTIONS_HEIGHT * (option + 0.5) // len(self.options) - text.get_height() // 2))


        window.blit(menu, (SCREEN_WIDTH // 2 - MENU_OPTIONS_WIDTH // 2, menu_Y))

