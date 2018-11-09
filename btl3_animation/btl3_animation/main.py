import sys
import pygame
import char

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

class Game():

    width = 1280
    height = 960

    def __init__(self):
        self.pygame = pygame

    def init(self):
        self.pygame.init()
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = self.pygame.time.Clock()
        self.time_step = 0
        # TODO: init sprite, tile,...
        #self.tilemap = tmx.load("map.tmx", self.screen.get_size())
        #self.sprites = tmx.Layer()
        self.player = char.Char()
        self.all_sprites = pygame.sprite.Group(self.player)
        #self.tilemap.layers.append(self.sprites)

    def run(self):
        # main game loop
        while True:
            # hold frame rate at 60 fps
            dt = self.clock.tick(60)
            self.time_step += 1
            # enumerate event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # sprite handle event
                self.handle(event)

            self.update(dt)
            # re-draw screen
            self.draw(self.screen)

    def draw(self, screen):
        screen.fill((95, 183, 229)) # sky color
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("Game", 1, (255, 0, 0))
            textpos = text.get_rect(centerx=self.width/2)
            self.screen.blit(text, textpos)
        # TODO: sprite tilemap
        #self.tilemap.set_focus(0, 480)
        #self.tilemap.draw(screen)
        self.all_sprites.draw(screen);
        self.pygame.display.flip()

    def update(self, dt):
        self.all_sprites.update(dt)
        pass

    def handle(self, event):
        self.player.handle(event)
        pass

if __name__ == '__main__':
    g = Game()
    g.init()
    g.run()
