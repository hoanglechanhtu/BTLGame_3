import  pygame
from Camera import *
from Map import  *
explosion =  [pygame.transform.scale(pygame.image.load('asset/Enemy/Particle/Explosion1.png'),(playerSize[0]*3,playerSize[1]*3)),pygame.transform.scale(pygame.image.load('asset/Enemy/Particle/Explosion2.png'),(playerSize[0]*3,playerSize[1]*3)),pygame.transform.scale(pygame.image.load('asset/Enemy/Particle/Explosion3.png'),(playerSize[0]*3,playerSize[1]*3)),pygame.transform.scale(pygame.image.load('asset/Enemy/Particle/Explosion4.png'),(playerSize[0]*3,playerSize[1]*3))]
class Effect:
    def __init__(self,x,y,effect,t,numberOfSprite,env):
        self.env = env
        env.effects.append(self)
        self.x = x
        self.y = y
        self.effect = effect
        self.animationCount = t
        self.numberOfSprite = numberOfSprite
    def draw(self,win):
        pass
    def update(self):
        pass
    def worldToCamera(self):
        return (self.x - camera.deltax, self.y - camera.deltay)
class Explosion(Effect,object):
    def __init__(self,x,y,effect,t,numberOfSprite,env):
        super(Explosion,self).__init__(x,y,effect,t,numberOfSprite,env)
    def update(self):
        self.animationCount+=1
        if self.animationCount > 7:
            self.animationCount = 7
            self.env.removeEffect(self)
    def draw(self,win):

        #TODO automaticly calculate animation
        win.blit(self.effect[self.animationCount//2], (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))