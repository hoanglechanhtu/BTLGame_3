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
up_tile_normal = pygame.transform.scale(pygame.image.load('asset/Environment/UpTileNormal.png'),(IMG_WIDTH, IMG_HEIGHT))

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
        self.tile_array = [[0 for i in range(0, 300)] for j in range(0, 95)]

    def build_ground_no_grass(self, top_left_index_X, top_left_index_Y, length, depth):
        # the rest is simply rocks
        for i in range(top_left_index_Y - depth, top_left_index_Y):
            for j in range(top_left_index_X, top_left_index_X + length):
                self.tile_array[NUM_TILES_LVL_VERTICAL - 2 - i][j] = Tile('center', j, NUM_TILES_LVL_VERTICAL - 2 - i)
                self.tile_array[NUM_TILES_LVL_VERTICAL - 2 - i][j].set_img(center_tile)

    def build_water(self, top_left_index_X, top_left_index_Y, length, depth):
        for i in range(top_left_index_Y - depth, top_left_index_Y):
            for j in range(top_left_index_X, top_left_index_X + length):
                self.tile_array[NUM_TILES_LVL_VERTICAL - 2 - i][j] = Tile('water', j, NUM_TILES_LVL_VERTICAL - 2 - i)
                self.tile_array[NUM_TILES_LVL_VERTICAL - 2 - i][j].set_img(up_tile_normal)

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

    def build_tile_with_type(self, top_left_index_X, top_left_index_Y, type):
        self.tile_array[NUM_TILES_LVL_VERTICAL - 1 - top_left_index_Y][top_left_index_X] = Tile(type, top_left_index_X, NUM_TILES_LVL_VERTICAL - 1 - top_left_index_Y)

    def draw(self, index_list):
        count = 0;

        for layer in self.tile_array:
            for block in layer:
                if (isinstance(block, Tile)):
                    block.draw()


game_map = Map()
game_map.build_ground_with_grass(0,3,25,4)
game_map.build_tile_with_type(20, 4, 'enemy1')
game_map.build_ground_with_grass(25,8,10,9)
game_map.build_ground_with_grass(35,3,10,4)
game_map.build_ground_with_grass(45,12,10,13)
game_map.build_ground_with_grass(55,3, 15,4)
game_map.build_tile_with_type(65, 4, 'enemy1')

game_map.build_ground_with_grass(72,9,16,4)
game_map.build_tile_with_type(80, 10, 'upgrade')
game_map.build_ground_with_grass(90,24,3,25)
game_map.build_ground_with_grass(93,3,50,4)
game_map.build_tile_with_type(110, 4, 'enemy1')
game_map.build_tile_with_type(125, 4, 'enemy1')

game_map.build_ground_with_grass(93,3,50,4)
game_map.build_ground_with_grass(98,23,10,3)
game_map.build_ground_with_grass(111,20,10,3)
game_map.build_tile_with_type(117, 21, 'enemy1')

game_map.build_tile_with_type(135, 4, 'box')
game_map.build_water(143,2,27,3)
game_map.build_tile_with_type(160,3, 'enemy5')
game_map.build_ground_with_grass(165,3,50,4)
game_map.build_ground_with_grass(185,8,3,5)
game_map.build_ground_with_grass(192,11,10,3)
game_map.build_ground_with_grass(205,15,10,3)
game_map.build_tile_with_type(195, 21, 'enemy3')



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