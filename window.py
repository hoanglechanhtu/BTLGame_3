import pygame
from Map import  *
from GameObject import *
from Enviroment import *
from Setup import *
import math
import random
from Particle import *
from start_screen import *

(width,height) = (SCREEN_WIDTH,SCREEN_HEIGHT)
pygame.mixer.music.load('asset/Music/backgroundMusic.mp3')
##header file


pygame.mixer.music.play(-1)

pygame.display.set_caption('Tutorial')
background_colour = (255,255,255)
win.fill(background_colour)

pygame.display.flip()
running = True

numberOfParticle = 10
env = Enviroment(width,height)
env.addFunctions1(['move','drag','gravity'])
env.addFunctions2(['collide'])
d = 0

pygame.font.init()

char = Player(playerStartPosition[0]+100,playerStartPosition[1],playerSize[0],playerSize[1],env)
env.setUpPlayer(char)
d=0
for layer in game_map.tile_array:
    for tile in layer:
      if isinstance(tile,Tile):
        width = IMG_WIDTH
        height = IMG_HEIGHT
        mass = 100

        x = tile.getX()
        y = tile.getY()
        if tile.type == "center" or tile.type == "grass":

            particle= Ground(x, y, width, height, env)
            particle.tile = tile
        elif tile.type == "water":
            particle = Water(x, y, width, height, env)
            particle.tile = tile
        elif tile.type == "box":
           box = Box(x,y,playerSize[0],playerSize[1],env)

        elif tile.type == "enemy1":
            enemy = Enemy(x,y,playerSize[0],playerSize[1],char,env)
            i = random.randint(0,1)
            if i > 0.5:
                enemy.moveLeft()
        elif tile.type == "enemy2":
            enemy = MachineGun(x, y, playerSize[0]*2, playerSize[1]*2, char, env)
            i = random.randint(0, 1)
            if i > 0.5:
                enemy.moveLeft()
        elif tile.type == 'enemy4':
            boss = Boss(x, y, playerSize[0] * 5, playerSize[1] * 3, char,env)
        elif tile.type == 'enemy5':
            p = BoxTrigger(x,y,playerSize[0],playerSize[1],env)

        elif tile.type == 'upgrade':
            p = UpgradeTrigger(x,y,playerSize[0],playerSize[1],env)
        elif tile.type == 'enemy6':
            d = DuTrigger(x,y,playerSize[0],playerSize[1],env)

print("number " + str(d))


menu = StartMenu()
isIntro = True
isGameOver = False

clock = pygame.time.Clock()


delta = updateRate

selectedParticle = None
first = 0
last = 0
while running:
    if isIntro:
        clock.tick(10)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keys[pygame.K_DOWN]:
            menu.change_option(True)
        if keys[pygame.K_UP]:
            menu.change_option(False)

        if keys[pygame.K_RETURN]:
            if (menu.chosen_option == 0):
                isIntro = False
            elif menu.chosen_option == len(menu.options) - 1:
                running = False
        menu.draw(win, 550)
    elif GameState.getInstance().is_game_over():
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            isIntro = True
            GameState.getInstance().reset()

        GameState.getInstance().draw_game_over(win, 750)
    elif GameState.getInstance().is_game_won():
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            isIntro = True
            GameState.getInstance().reset()

        GameState.getInstance().draw_game_win(win, 750)
    else:
        last = pygame.time.get_ticks()/1000.0
        #clock.tick(27)
        first = last
        win.fill(env.colour)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                selectedParticle= env.findParticles(mouseX,mouseY)
            elif event.type == pygame.MOUSEBUTTONUP:
                char.shot()
                selectedParticle = None
        if keys[pygame.K_a]:
            char.moveLeft()

        if keys[pygame.K_d]:
            char.moveRight()
        if keys[pygame.K_LEFT]:
            camera.moveLeft()
        if keys[pygame.K_RIGHT]:
            camera.moveRight()
        if keys[pygame.K_DOWN]:
            camera.moveDown()
        if keys[pygame.K_UP]:
            camera.moveUp()

        if keys[pygame.K_w]:
            char.jump()
        if keys[pygame.K_v]:
            pass#char.shot()

        camera.update(char)

        env.update()

        redrawGameWindow()
        #char.draw(win)
        env.draw()
        #uncomment to draw physics box
        # for p in env.particles:
        #
        #     if p.type == 1:
        #
        #
        #         pygame.draw.circle(win, p.colour, (int(p.x), int(p.y)), p.r, p.thickness)
        #     if p.type == 2:
        #         pygame.draw.rect(win,p.colour,(int(p.x - camera.deltax),int(p.y - camera.deltay),int(p.width),int(p.height)),p.thickness)
        #         pass


    #
    # if selectedParticle:
    #     (mouseX,mouseY) = pygame.mouse.get_pos()
    #     selectedParticle.moveMouse(mouseX,mouseY)
    #








    pygame.display.update()
    #clock.tick(1 / updateRate)
