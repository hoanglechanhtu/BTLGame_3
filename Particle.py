import pygame
import math
import random
from params import *
from Setup  import  *
from Effect import *
import  GameObject as go

def addVector(vector1 , vector2):
        x = math.sin(vector1.angle)*vector1.length + math.sin(vector2.angle)*vector2.length
        y = math.cos(vector1.angle) * vector1.length + math.cos(vector2.angle) * vector2.length
        length = math.hypot(x,y)
        angle = 0.5*math.pi - math.atan2(y,x)
        return vector(angle,length)

def boxCollideBox(p1,p2):

    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dy, dx)
    if p1.getMinX()  < p2.getMaxX() and p1.getMaxX() > p2.getMinX()and p1.getMinY()<p2.getMaxY() and p1.getMaxY() > p2.getMinY() :
        if not p1.parent == None and not p2.parent== None:
            if  p1.parent.name == "Water" and p2.parent.name == "Player":
                p2.parent.kill()
                return
            if p2.parent.name == "Water" and p1.parent.name == "Player":
                p1.parent.kill()
                return
        if p1.isTrigger:
            p1.hit(p2)
            return
        if p2.isTrigger:
            p2.hit(p1)
            return
        # if p2.y < p1.y :
        #     p2.isInAir = False
        # if p2.y > p1.y:
        #     p1.isInAir = False
        if p1.getMaxX() < p2.getMinX()  + 5 or p1.getMinX() + 10 > p2.getMaxX(): #collide offset
            if p1.isInAir:
                p1.isClimb = True
            p1.isInAir = False

        else:
            p1.isClimb = False
        if p1.getMaxY() < p2.getMinY() +5 :
            p1.isInAir = False
            p1.isClimb = False

        tangent = math.atan2(dy, dx)
        angle = tangent + 0.5 * math.pi
        totalMass = p1.mass + p2.mass
        # TODO calculate the overlap distance
        overlap = 0.05 * (p1.width + p2.height - distance + 1)

        if not p1.static:

            p1.hit(p2)
            p1.x += math.sin(angle) * overlap
            p1.y -= math.cos(angle) * overlap
        if not p2.static:
            p2.hit(p1)
            p2.x -= math.sin(angle) * overlap
            p2.y += math.cos(angle) * overlap
        p1.angle = 2 * tangent - p1.angle
        p2.angle = 2 * tangent - p2.angle
        vectorP1 = addVector(vector(p1.angle, p1.speed * (p1.mass - p2.mass) / totalMass),
                             vector(angle, 2 * p2.speed * p2.mass / totalMass))
        (p1.angle, p1.speed) = (vectorP1.angle, vectorP1.length)
        vectorP2 = addVector(vector(p2.angle, p2.speed * (p2.mass - p1.mass) / totalMass),
                             vector(angle + math.pi, 2 * p1.speed * p1.mass / totalMass))
        (p2.angle, p2.speed) = (vectorP2.angle, vectorP2.length)

        p1.speed *= elasticity
        p2.speed *= elasticity


def circleCollideCircle(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dy, dx)
    if distance < p1.r + p2.r:

        tangent = math.atan2(dy, dx)
        angle = tangent + 0.5 * math.pi
        totalMass = p1.mass + p2.mass
        overlap = 0.5 * (p1.r + p2.r - distance + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap
        p1.angle = 2 * tangent - p1.angle
        p2.angle = 2 * tangent - p2.angle
        vectorP1 = addVector(vector(p1.angle, p1.speed * (p1.mass - p2.mass) / totalMass),
                             vector(angle, 2 * p2.speed * p2.mass / totalMass))
        (p1.angle, p1.speed) = (vectorP1.angle, vectorP1.length)
        vectorP2 = addVector(vector(p2.angle, p2.speed * (p2.mass - p1.mass) / totalMass),
                             vector(angle + math.pi, 2 * p1.speed * p1.mass / totalMass))
        (p2.angle, p2.speed) = (vectorP2.angle, vectorP2.length)

        p1.speed *= elasticity
        p2.speed *= elasticity
#p1 box
#p2 circle
def boxCollideCircle(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dy, dx)
    if p1.getMinX() < p2.getMaxX() and p1.getMaxX() > p2.getMinX() and p1.getMinY() < p2.getMaxY() and p1.getMaxY() > p2.getMinY():

        tangent = math.atan2(dy, dx)
        angle = tangent + 0.5 * math.pi
        totalMass = p1.mass + p2.mass
        overlap = 0.5 * (p1.width + p2.r - distance + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap
        p1.angle = 2 * tangent - p1.angle
        p2.angle = 2 * tangent - p2.angle
        vectorP1 = addVector(vector(p1.angle, p1.speed * (p1.mass - p2.mass) / totalMass),
                             vector(angle, 2 * p2.speed * p2.mass / totalMass))
        (p1.angle, p1.speed) = (vectorP1.angle, vectorP1.length)
        vectorP2 = addVector(vector(p2.angle, p2.speed * (p2.mass - p1.mass) / totalMass),
                             vector(angle + math.pi, 2 * p1.speed * p1.mass / totalMass))
        (p2.angle, p2.speed) = (vectorP2.angle, vectorP2.length)

        p1.speed *= elasticity
        p2.speed *= elasticity
def collide(p1,p2):
    # bullet go through enemy if come from enemy
    if not p1.parent == None:
        if not p2.parent == None:
            if p1.parent.name == 'Bullet' and p1.parent._from == p2.parent.name:
                return
            if p2.parent.name == 'Bullet' and p2.parent._from == p1.parent.name:
                return

    boxCollideBox(p1, p2)


class Particle:
    def __init__(self, x,y,type,size=1,mass=1):
        self.isTrigger = False
        self.parent = None
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0,0,255)
        self.type = type
        self.thickness = 1
        self.speed =defaultSpeed
        self.angle = math.pi/2
        self.mass = mass
        self.drag = drag
        self.static =  False
        self.isInAir = False
        self.isClimb = False
        self.isAffectByGravity = True
    def hit(self,particle):
        if self.parent == None:
            return
        self.parent.hit(particle)
    def jump(self):

        if self.isInAir:
            return
        else:
            self.isClimb = False
            self.isInAir = True
            self.firstMove = True
            self.accelerate(jumpVector)
    def moveLeft(self):

        if self.isInAir:
            if self.speed > 2 * moveSpeed:
                self.speed = 2 * moveSpeed
            temp = self.speed
            self.accelerate(vector( -math.pi / 2,moveSpeed*airControllLoss))
            self.speed = temp
            return
        else:
            if self.speed > moveSpeed:
                self.speed =  moveSpeed
            self.accelerate(vector(-math.pi/2,moveSpeed))
            # self.speed = moveSpeed
            # self.angle = -math.pi / 2
    def moveRight(self):

        if self.isInAir:
            if self.speed > 2 * moveSpeed:
                self.speed = 2 * moveSpeed
            self.accelerate(vector(math.pi / 2,moveSpeed*airControllLoss))
            return
        else:
            if self.speed >  moveSpeed:
                self.speed = moveSpeed
            self.accelerate(vector( math.pi / 2,moveSpeed))
            # self.speed = moveSpeed
            # self.angle = math.pi / 2
    def moveDown(self):
        pass
    def moveUp(self):
        pass
    def experienceGravity(self,vector1):
        if self.isAffectByGravity:
            self.accelerate(vector1)
    def accelerate(self, vector1):

        val = addVector(vector(self.angle,self.speed),vector1)
        (self.angle, self.speed) = (val.angle,val.length)
    def experienceDrag(self):
        self.speed *= self.drag
    def move(self):

        if not self.static :
            self.x += math.sin(self.angle)*self.speed

            self.y -= math.cos(self.angle)*self.speed

        if not self.parent == None:
            self.parent.updatePosition()


    def bounce(self,width,height):
        pass
    def moveMouse(self,x,y):
        dx = x - self.x
        dy = y - self.y

        self.angle = 0.5 * math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) *0.1
# type = 1 circle
# type = 2 box
class CircleParticle(Particle,object):
    def __init__(self,x,y,r,mass=1):

        self.r = r
        self.size = math.pi * r**2/2
        self.type = 1
        self.mass = mass
        super(CircleParticle,self).__init__(x,y,self.type,self.size,self.mass)
    def getMaxX(self):
        return self.x + self.r
    def getMinX(self):
        return self.x
    def getMaxY(self):
        return self.y +self.r
    def getMinY(self):
        return self.y
    def bounce(self,width,height):

        if self.x > width - self.r:
            self.speed*= elasticity
            self.x = 2 * (width - self.r) - self.x
            self.angle = - self.angle
        elif self.x < self.r:
            self.speed *= elasticity
            self.x = 2 * self.r - self.x
            self.angle = - self.angle
        if self.y > height - self.r:
            self.speed *= elasticity
            self.y = 2 * (height - self.r) - self.y
            self.angle = math.pi - self.angle
        elif self.y < self.r:
            self.speed *= elasticity
            self.y = 2 * self.r - self.y
            self.angle = math.pi - self.angle
class BoxParticle(Particle,object):
    def __init__(self,x,y,width,height,mass = 1):

        self.width = width
        self.height = height
        self.type = boxType
        self.size = self.width*self.height
        self.mass = mass
        super(BoxParticle, self).__init__(x, y, self.type, self.size, self.mass)
    def getMaxX(self):
        return self.x + self.width
    def getMinX(self):
        return self.x
    def getMaxY(self):
        return self.y +self.height
    def getMinY(self):
        return self.y
    def bounce(self,width,height):

        if self.x > width - self.width:
            #self.isInAir = False
            self.hit(None)
            self.speed*= elasticity
            self.x = 2 * (width - self.width) - self.x
            self.angle = - self.angle
        elif self.x < 0:
            #self.isInAir = False
            self.hit(None)
            self.speed *= elasticity
            self.x = 2 * self.width - self.x
            self.angle = - self.angle
        if self.y > height - self.height:
            self.isInAir = False
            self.hit(None)
            self.speed *= elasticity
            self.y = 2 * (height - self.height) - self.y
            self.angle = math.pi - self.angle
        elif self.y < 0:
           # self.isInAir = False
            self.hit(None)
            self.speed *= elasticity
            self.y = 2 * self.height - self.y
            self.angle = math.pi - self.angle



class BoxTrigger(BoxParticle, object):
    def __init__(self,x,y,width,height,env,mass = 1):
        super(BoxTrigger, self).__init__(x, y, width, height)
        self.static = True
        self.isAffectByGravity = False
        self.isTrigger = True
        self.env = env
        self.times = 1
        self.currentTime = 0
        self.isHit = False
        self.env.particles.append(self)
    def hit(self, particle):
        if particle.parent.name == 'Player':
            if self.currentTime < self.times:
                p = TruckEffect(self.x+1000, self.y - 120, truckRun, 1, 1, self.env)

                self.currentTime +=1
            self.isHit = True
class DuTrigger(BoxParticle, object):
    def __init__(self,x,y,width,height,env,mass = 1):
        super(DuTrigger, self).__init__(x, y, width, height)
        self.static = True
        self.isAffectByGravity = False
        self.isTrigger = True
        self.env = env
        self.times = 1
        self.currentTime = 0
        self.numberOfEnemy = random.randint(3,5)
        self.isHit = False
        self.env.particles.append(self)
    def hit(self, particle):
        if particle.parent.name == 'Player':
            if self.currentTime < self.times:
                i = -5
                while self.numberOfEnemy >0:
                    e = go.Enemy(self.x+i*100,self.y- 1000 - random.randint(-200,200),playerSize[0],playerSize[1],self.env.player,self.env)
                    self.numberOfEnemy -= 1
                    i+=1
                self.currentTime +=1
            self.isHit = True
class CoinTrigger(BoxParticle, object):
    def __init__(self,x,y,width,height,env,mass = 1):
        super(CoinTrigger, self).__init__(x, y, width, height)
        self.static = True
        self.isAffectByGravity = False
        self.isTrigger = True
        self.env = env
        self.env.particles.append(self)
        self.times = 1
        self.currentTime = 0
        self.isHit = False
        self.c = CoinEffect(self.x,self.y,coin,1,1,self.env)
    def hit(self, particle):
        if particle.parent.name == 'Player':
            if self.currentTime < self.times:
                # add coin to player
                self.env.player.coin +=1
                self.env.removeParticle(self)
                self.env.removeEffect(self.c)
                self.currentTime +=1
            self.isHit = True

class UpgradeTrigger(BoxParticle, object):
    def __init__(self,x,y,width,height,env,mass = 1):
        super(UpgradeTrigger, self).__init__(x, y, width, height)
        self.static = True
        self.isAffectByGravity = False
        self.isTrigger = True
        self.env = env
        self.env.particles.append(self)
        self.times = 1
        self.currentTime = 0
        self.isHit = False
        self.c = CoinEffect(self.x,self.y,upgrade,1,1,self.env)
    def hit(self, particle):
        if particle.parent.name == 'Player':
            if self.currentTime < self.times:
                self.env.player.upgrade +=1
                self.env.player.coin +=1
                self.env.removeParticle(self)
                self.env.removeEffect(self.c)
                self.currentTime +=1
            self.isHit = True