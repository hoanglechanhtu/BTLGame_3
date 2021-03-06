import  pygame
from Camera import *
from Map import  *
import GameObject as go

explosion =  [pygame.transform.scale(pygame.image.load('asset/Enemy/Particle/Explosion1.png'),(playerSize[0]*3,playerSize[1]*3)),pygame.transform.scale(pygame.image.load('asset/Enemy/Particle/Explosion2.png'),(playerSize[0]*3,playerSize[1]*3)),pygame.transform.scale(pygame.image.load('asset/Enemy/Particle/Explosion3.png'),(playerSize[0]*3,playerSize[1]*3)),pygame.transform.scale(pygame.image.load('asset/Enemy/Particle/Explosion4.png'),(playerSize[0]*3,playerSize[1]*3))]
truckRun = [pygame.transform.scale(pygame.image.load('asset/Enemy/Vehicle/Truck1.png'),(playerSize[0]*3,playerSize[1]*3)),pygame.transform.scale(pygame.image.load('asset/Enemy/Vehicle/Truck2.png'),(playerSize[0]*3,playerSize[1]*3))]
coin = [pygame.transform.scale(pygame.image.load('asset/Environment/coin1.png'),(playerSize[0]//2,playerSize[1]//2)),pygame.transform.scale(pygame.image.load('asset/Environment/coin2.png'),(playerSize[0]//2,playerSize[1]//2 ))]
upgrade = [pygame.transform.scale(pygame.image.load('asset/Environment/upgrade.png'),(playerSize[0],playerSize[1])),pygame.transform.scale(pygame.image.load('asset/Environment/upgrade1.png'),(playerSize[0],playerSize[1] ))]
explosionSound =  pygame.mixer.Sound('asset/Music/Explosion.wav')
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
        explosionSound.play()
    def update(self):
        self.animationCount+=1
        if self.animationCount > 7:
            self.animationCount = 7
            self.env.removeEffect(self)
    def draw(self,win):

        #TODO automaticly calculate animation
        win.blit(self.effect[self.animationCount//2], (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
class CoinEffect(Effect,object):
    def __init__(self,x,y,effect,t,numberOfSprite,env):
        super(CoinEffect,self).__init__(x,y,effect,t,numberOfSprite,env)
        self.timeToStop = 1000

    def kill(self):
        self.env.removeEffect(self)
    def update(self):
        self.timeToStop -= 1.0/27.0
        self.animationCount+=1
        if self.animationCount > 7:
            self.animationCount = 1
        if self.timeToStop <0:
            self.kill()
    def draw(self,win):
        win.blit(self.effect[self.animationCount//4], (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))

class TruckEffect(Effect,object):
    def __init__(self,x,y,effect,t,numberOfSprite,env):
        super(TruckEffect,self).__init__(x,y,effect,t,numberOfSprite,env)
        self.timeToStop = 5
        self.spawnEnemyTime = 1
        self.numberOfEnemy = 5
    def update(self):
        if self.numberOfEnemy <0:
            return
        self.timeToStop -= 1.0/27.0
        if self.timeToStop>0:
            self.x = self.x - 5
        else:
            self.timeToStop = 0
            self.spawnEnemyTime -= 1.0/27.0
            if self.spawnEnemyTime <0:
                e = go.Enemy(self.x+200,self.y+50,playerSize[0],playerSize[1],self.env.player,self.env)
                e.changeState(idle)
                e.moveLeft()

                self.spawnEnemyTime = 2
                self.numberOfEnemy -=1
            return
        self.animationCount+=1
        if self.animationCount > 7:
            self.animationCount = 1
            #self.env.removeEffect(self)
    def draw(self,win):

        #TODO automaticly calculate animation
        if self.timeToStop >0:
            win.blit(self.effect[self.animationCount//4], (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        else:
            win.blit(self.effect[0],
                     (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
