import pygame
from  params import *
from  Camera import *

pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
camera = Camera(640,360)
#load assets
box = pygame.transform.scale(pygame.image.load('asset/Environment/Box.png'),(playerSize[0], playerSize[1]))
bridge = pygame.transform.scale(pygame.image.load('asset/Environment/Bridge.png'), (IMG_WIDTH, IMG_HEIGHT))
center_tile = pygame.transform.scale(pygame.image.load('asset/Environment/ground_no_grass.jpg'), (IMG_WIDTH, IMG_HEIGHT))
left_tile = pygame.image.load('asset/Environment/LeftTile.png')
right_tile = pygame.image.load('asset/Environment/RightTile.png')
down_tile_center = pygame.image.load('asset/Environment/DownTileCenter.png')
down_tile_left = pygame.image.load('asset/Environment/DownTileLeft.png')
down_tile_right = pygame.image.load('asset/Environment/DownTileRight.png')
ladder = pygame.image.load('asset/Environment/ladder.png')
up_tile_grass = pygame.transform.scale(pygame.image.load('asset/Environment/ground_with_grass_2.jpg'), (IMG_WIDTH, IMG_HEIGHT))
up_tile_normal = pygame.image.load('asset/Environment/UpTileNormal.png')

#load background
bg1 = pygame.transform.scale(pygame.image.load('asset/Environment/background/plx-1.png') , (SCREEN_WIDTH, SCREEN_HEIGHT))
bg2 = pygame.transform.scale(pygame.image.load('asset/Environment/background/plx-2.png') , (SCREEN_WIDTH, SCREEN_HEIGHT))
bg3 = pygame.transform.scale(pygame.image.load('asset/Environment/background/plx-3.png') , (SCREEN_WIDTH, SCREEN_HEIGHT))
bg4 = pygame.transform.scale(pygame.image.load('asset/Environment/background/plx-4.png') , (SCREEN_WIDTH, SCREEN_HEIGHT))
bg5 = pygame.transform.scale(pygame.image.load('asset/Environment/background/plx-5.png') , (SCREEN_WIDTH, SCREEN_HEIGHT))

canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas.blit(bg1,(0,0))
canvas.blit(bg2,(0,0))
canvas.blit(bg3,(0,0))
canvas.blit(bg4,(0,0))
canvas.blit(bg5,(0,0))

clock = pygame.time.Clock()

class Tile:
    def __init__(self, type, index_X, index_Y):
        self.original_X = index_X
        self.original_Y = index_Y
        self.index_X = index_X
        self.index_Y = index_Y
        self.img = None
        self.type = type

    def draw(self):
        if self.type == 0:
            return
        if self.img is not None:
            win.blit(self.img, (self.index_X * IMG_WIDTH - camera.deltax, self.index_Y * IMG_HEIGHT - camera.deltay))

    def set_pos_indx_X(self, x):
        self.index_X = x

    def set_pos_indx_Y(self, y):
        self.index_Y = y

    def getX(self):
        return self.index_X*IMG_WIDTH

    def getY(self):
        return self.index_Y*IMG_HEIGHT

    def set_img(self, img):
        self.img = img
class Map:
    def __init__(self):
        self.tile_array = [[0 for i in range(0, 100)] for j in range(0, 95)]

    def build_ground_no_grass(self, top_left_index_X, top_left_index_Y, length, depth):
        # the rest is simply rocks
        for i in range(top_left_index_Y - depth, top_left_index_Y):
            for j in range(top_left_index_X, top_left_index_X + length):
                self.tile_array[NUM_TILES_LVL_VERTICAL - 2 - i][j] = Tile('center', j, NUM_TILES_LVL_VERTICAL - 2 - i)
                self.tile_array[NUM_TILES_LVL_VERTICAL - 2 - i][j].set_img(center_tile)

    def build_ground_with_grass(self, top_left_index_X, top_left_index_Y, length, depth):
        #length is the number of tiles horizontally for this section of the ground
        #depth is the number of tiles vertically

        #the first layer is grass
        for i in range(top_left_index_X, top_left_index_X + length):
            self.tile_array[NUM_TILES_LVL_VERTICAL - 1 - top_left_index_Y][i] \
                = Tile('grass', i, NUM_TILES_LVL_VERTICAL - 1 - top_left_index_Y)
            self.tile_array[NUM_TILES_LVL_VERTICAL - 1 - top_left_index_Y][i].set_img(up_tile_grass)

        self.build_ground_no_grass(top_left_index_X, top_left_index_Y - 1, length, depth - 1)

    def build_box(self, top_left_index_X, top_left_index_Y):
        self.tile_array[NUM_TILES_LVL_VERTICAL - 1 - top_left_index_Y][top_left_index_X] = Tile('box', top_left_index_X, NUM_TILES_LVL_VERTICAL - 1 - top_left_index_Y)

    def build_enemy(self, top_left_index_X, top_left_index_Y, enemyType):
        self.tile_array[NUM_TILES_LVL_VERTICAL - 1 - top_left_index_Y][top_left_index_X] = Tile(enemyType, top_left_index_X, NUM_TILES_LVL_VERTICAL - 1 - top_left_index_Y)

    def draw(self, index_list):
        count = 0;

        for layer in self.tile_array:
            for block in layer:
                if (isinstance(block, Tile)):
                    block.draw()


game_map = Map()
game_map.build_ground_with_grass(0,11,10,2)
game_map.build_box(6, 4)
game_map.build_box(7, 4)
game_map.build_box(8, 4)
game_map.build_ground_with_grass(6,3,4,4)
game_map.build_ground_no_grass(0,9,6,10)
game_map.build_enemy(25, 22, 'enemy1')
game_map.build_enemy(32, 30, 'enemy2')
game_map.build_enemy(35, 30, 'enemy1')

game_map.build_box(41,18)
game_map.build_box(42,18)
game_map.build_box(43,18)
game_map.build_box(44,18)
game_map.build_box(45,18)
game_map.build_box(41,19)
game_map.build_box(42,19)
game_map.build_box(43,19)
game_map.build_box(44,19)
game_map.build_box(41,20)
game_map.build_box(42,20)
game_map.build_box(43,20)
game_map.build_box(41,21)
game_map.build_box(42,21)

game_map.build_enemy(49, 18, 'enemy3')
game_map.build_enemy(60, 14, 'enemy1')

game_map.build_enemy(65, 14, 'enemy1')
game_map.build_enemy(69, 14, 'enemy2')
game_map.build_enemy(75, 14, 'enemy3')

game_map.build_enemy(65, 24, 'enemy3')
game_map.build_enemy(69, 24, 'enemy3')
game_map.build_enemy(72, 24, 'enemy2')

game_map.build_enemy(62, 28, 'enemy1')
game_map.build_enemy(73, 28, 'enemy1')
game_map.build_enemy(79, 28, 'enemy2')
game_map.build_enemy(83, 28, 'enemy1')

game_map.build_enemy(75, 31, 'enemy1')
game_map.build_enemy(82, 31, 'enemy3')

game_map.build_enemy(35,40,'enemy4')
game_map.build_enemy(35,35,'enemy5')

game_map.build_ground_with_grass(19,11,4,12)
game_map.build_ground_with_grass(23,21,4,22)
game_map.build_ground_with_grass(27,29,10,30)
game_map.build_ground_with_grass(37,25,4,26)
game_map.build_ground_with_grass(41,17,10,4)
game_map.build_ground_no_grass(41,13,8,2)
game_map.build_ground_no_grass(41,11,6,2)
game_map.build_ground_no_grass(41,9,4,10)

game_map.build_ground_with_grass(55,13,30,14)
game_map.build_box(81,14)
game_map.build_box(82,14)
game_map.build_box(83,14)
game_map.build_box(84,14)
game_map.build_box(82,15)
game_map.build_box(83,15)

game_map.build_box(75,24)
game_map.build_box(76,24)
game_map.build_box(75,25)
game_map.build_box(76,25)

game_map.build_box(75,24)
game_map.build_box(76,24)
game_map.build_box(75,25)
game_map.build_box(76,25)

game_map.build_ground_no_grass(85, 13, 5, 2)
game_map.build_ground_no_grass(85, 18, 7, 5)
game_map.build_ground_with_grass(92, 18, 2, 1)
game_map.build_ground_with_grass(92, 19, 1, 1)
game_map.build_ground_no_grass(80, 23, 12, 5)

game_map.build_ground_no_grass(60, 23, 19, 3)
game_map.build_ground_no_grass(62, 20, 16, 2)
game_map.build_ground_no_grass(73, 18, 3, 3)
game_map.build_ground_no_grass(65, 18, 3, 1)

game_map.build_ground_no_grass(60, 30, 1, 7)
game_map.build_ground_no_grass(91, 30, 1, 9)
game_map.build_ground_no_grass(62, 27, 4, 1)
game_map.build_ground_no_grass(68, 27, 6, 1)
game_map.build_ground_no_grass(71, 27, 19, 1)

game_map.build_ground_no_grass(61, 30, 8, 1)
game_map.build_ground_no_grass(72, 30, 7, 1)
game_map.build_ground_no_grass(80, 30, 5, 1)
game_map.build_ground_no_grass(87, 30, 4, 1)

game_map.build_ground_no_grass(65, 33, 16, 1)
game_map.build_ground_no_grass(82, 33, 9, 1)

game_map.build_ground_no_grass(64, 40, 1, 10)
game_map.build_ground_no_grass(90, 40, 1, 10)


def redrawGameWindow():
    win.blit(canvas, (0,0))

    game_map.draw(camera.get_tiles_indexes_in_camera_frame())
    camera.draw(win)
    pygame.display.flip()


first = 0
last = 0
run = True
# while run:
#     clock.tick(200)
#     last = pygame.time.get_ticks()/1000.0
#
#     print(1.0/(last - first))
#     first = last
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_a]:
#         camera.moveLeft(20)
#
#     if keys[pygame.K_d]:
#         camera.moveRight(20)
#
#     if keys[pygame.K_w]:
#         camera.moveUp(20)
#
#     if keys[pygame.K_s]:
#         camera.moveDown(20)
#
#     redrawGameWindow()