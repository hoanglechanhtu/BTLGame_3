import pygame
from Setup import *
from  params import *

class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = SCREEN_HEIGHT - y
        self.startx = x
        self.starty = y
        self.deltax= 0
        self.deltay= LVL_HEIGHT - SCREEN_HEIGHT
        self.leftBorder = 50
        self.rightBorder = 50
        self.topBorder = 50
        self.bottomBorder = 50
    def moveLeft(self):
        self.x -=moveSpeed
        self.deltax = self.x - self.startx
    def moveRight(self):
        self.x += moveSpeed

        self.deltax = self.x - self.startx

    #here we simulate the movement of the camera from bottom up
    def moveUp(self):
        self.deltay -= moveSpeed

    def moveDown(self):
        self.deltay += moveSpeed

    def get_view_frame(self):
        return [self.x - SCREEN_WIDTH / 2, self.y + SCREEN_HEIGHT / 2]

    def draw(self, screen):
        pygame.draw.circle(screen, pygame.color.THECOLORS["white"], (int(self.x), int(SCREEN_HEIGHT // 2)), 5, 0);

    def update(self,player):

        if player.x > self.x +self.rightBorder:
            self.x += 5
        if player.x < self.x - self.leftBorder:
            self.x -= 5

        if player.y > self.deltay + self.bottomBorder + SCREEN_HEIGHT // 2:
            self.deltay += 2*moveSpeed
        if player.y < self.deltay - self.topBorder + SCREEN_HEIGHT // 2:
            self.deltay -= 2*moveSpeed

        self.deltax = self.x - self.startx

        if self.deltax < 0:
            self.deltax = 0

        # if (self.deltay > LVL_HEIGHT - SCREEN_HEIGHT):
        #     self.deltay = LVL_HEIGHT - SCREEN_HEIGHT

        # if player.y > self.y + self.topBorder:
        #     self.y +=
        #self.y = SCREEN_HEIGHT- player.y
    def get_tiles_indexes_in_camera_frame(self):
        #horizontal and vertical
        min_X_idx = 0
        max_X_idx = 0
        min_Y_idx = 0
        max_Y_idx = 0
        if (self.x - SCREEN_WIDTH / 2 >= 0):
            min_X_idx = (self.x - SCREEN_WIDTH / 2) // IMG_WIDTH;
            max_X_idx = min_X_idx + NUM_TILES_HORIZONTAL_SCR
        else:
            min_X_idx = 0
            max_X_idx = min_X_idx + NUM_TILES_HORIZONTAL_SCR

        if (self.x + SCREEN_WIDTH / 2 >= LVL_WIDTH):
            max_X_idx = NUM_TILES_LVL_HORIZONTAL - 1;
            min_X_idx = NUM_TILES_LVL_HORIZONTAL - 1 - NUM_TILES_HORIZONTAL_SCR

        if (self.y - SCREEN_HEIGHT / 2 >= 0):
            min_Y_idx = (self.y - SCREEN_HEIGHT / 2) // IMG_HEIGHT;
            max_Y_idx = min_Y_idx + NUM_TILES_VERTICAL_SCR
        else:
            min_Y_idx = 0
            max_Y_idx = min_Y_idx + NUM_TILES_VERTICAL_SCR

        if (self.y + SCREEN_HEIGHT/ 2 >= LVL_HEIGHT):
            max_Y_idx = NUM_TILES_LVL_VERTICAL - 1;
            min_Y_idx = NUM_TILES_LVL_VERTICAL - NUM_TILES_VERTICAL_SCR
        return [int(min_X_idx), int(max_X_idx),
                int(NUM_TILES_LVL_VERTICAL - 1 - max_Y_idx), int(NUM_TILES_LVL_VERTICAL - 1 - min_Y_idx)]
