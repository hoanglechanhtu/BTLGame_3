import  pygame
from Particle import *
from Enviroment import *
from Setup  import  *
from Effect import *
fireSound = pygame.mixer.Sound('asset/Music/fire.wav')
hitSound = pygame.mixer.Sound('asset/Music/hit.wav')
playerIdleLeft = pygame.transform.scale(pygame.image.load('asset/Char/1/Idle.png'),(playerSize[0],playerSize[1]))
playerDie = pygame.transform.scale(pygame.image.load('asset/Char/1/die.png'),(playerSize[0],playerSize[1]))
playerIdleRight =  pygame.transform.flip(playerIdleLeft,True,False)
playerRunLeft = [pygame.transform.scale(pygame.image.load('asset/Char/1/Run1.png'),(playerSize[0],playerSize[1])),pygame.transform.scale(pygame.image.load('asset/Char/1/Run2.png'),(playerSize[0],playerSize[1]))]
playerRunRight = [pygame.transform.flip(playerRunLeft[0],True,False),pygame.transform.flip(playerRunLeft[1],True,False)]
playerFireLeft = pygame.transform.scale(pygame.image.load('asset/Char/1/Fire.png'),(playerSize[0],playerSize[1]))
playerFireRight = pygame.transform.flip(playerFireLeft,True,False)
playerClimpLeft =  pygame.transform.scale(pygame.image.load('asset/Char/1/WallS.png'),(playerSize[0],playerSize[1]))
playerClimpRight = pygame.transform.flip(playerClimpLeft,True,False)
bullet =  pygame.transform.scale(pygame.image.load('asset/Environment/bullet.png'),(bulletSize[0],bulletSize[1]))
bullet2 =  pygame.transform.scale(pygame.image.load('asset/Environment/bullet.png'),(bulletSize[0]*2,bulletSize[1]*2))
bullet3 =  pygame.transform.scale(pygame.image.load('asset/Environment/bullet.png'),(bulletSize[0]*3,bulletSize[1]*3))
bullet4 =  pygame.transform.scale(pygame.image.load('asset/Environment/bulletMax.png'),(bulletSize[0]*3,bulletSize[1]*3))
bossBullet =  pygame.transform.scale(pygame.image.load('asset/Environment/bullet.png'),(bulletSize[0]*3,bulletSize[1]*3))
bossRight = [pygame.transform.scale(pygame.image.load('asset/Enemy/Boss/Heli1.png'),(playerSize[0]*5,playerSize[1]*4)),pygame.transform.scale(pygame.image.load('asset/Enemy/Boss/Heli2.png'),(playerSize[0]*5,playerSize[1]*4)),pygame.transform.scale(pygame.image.load('asset/Enemy/Boss/Heli3.png'),(playerSize[0]*5,playerSize[1]*4))]
bossLeft = [pygame.transform.flip(bossRight[0],True,False),pygame.transform.flip(bossRight[1],True,False),pygame.transform.flip(bossRight[2],True,False)]
boom = [pygame.image.load('asset/Enemy/Boss/Boom1.png'),pygame.image.load('asset/Enemy/Boss/Boom2.png'),pygame.image.load('asset/Enemy/Boss/Boom3.png'),pygame.image.load('asset/Enemy/Boss/Boom4.png')]
class GameObject:
    def __init__(self,x,y,width,height,env):
        self.name = "GameObject"
        self.x = x
        self.y = y
        self.env = env
        self.width = width
        self.height = height
        self.tile = None
    def draw(self,win):
        pass
    def kill(self):
        pass
    def hit(self,particle):
        pass

    def worldToCamera(self):
        return (self.x - camera.deltax, self.y - camera.deltay)
    def updatePosition(self):
        self.x = self.particle.x
        self.y = self.particle.y
    def update(self):
        pass
class Player(GameObject, object):
    def __init__(self,x,y,width,height,env):
        super(Player,self).__init__(x,y,width,height,env)
        self.coin = 0
        self.particle = BoxParticle(x,y,width,height)
        self.particle.static = False
        self.direction = Right
        self.env.particles.append(self.particle)
        self.particle.parent = self
        self.name = "Player"
        self.state = idle
        self.animationCount = 0
        self.shotCd = PlayerShotCd
        self.shotTimer = 0
        self.particle.isInAir =True
        self.upgrade = 0
    def kill(self):
        self.changeState(die)

    def changeState(self,state):
        if self.state == state:
            return
        self.state = state
        self.animationCount = 0
    def moveLeft(self):
        self.direction = Left
        self.particle.moveLeft()
        self.changeState(running)
    def moveRight(self):
        self.changeState(running)
        self.direction = Right
        self.particle.moveRight()
    def moveUp(self):
        pass
    def moveDown(self):
        pass
    def jump(self):
        self.particle.jump()
    def shot(self):

        if not self.shotTimer <= 0:
            return
        self.shotTimer = self.shotCd
        self.changeState(shot)
        if self.direction == Right:
            offset = self.width+ bulletOffset
        else:
            offset = -3*bulletOffset
        p = Bullet(self.particle.x+offset,self.particle.y + self.height/2 - self.upgrade*5,bulletSize[0],bulletSize[1],self.env,self.name)
        if self.upgrade == 1:
            p.setBullet(bullet2)
        elif self.upgrade == 2:
            p.setBullet(bullet3)
        elif self.upgrade == 3:
            p.setBullet(bullet4)
        p.shot(self.direction*math.pi/2)

    def hit(self,particle):
        #print "hit "+ particle.parent.name
        pass
    def update(self):
        if self.shotTimer <0:
            self.shotTimer = 0
        self.shotTimer -= 1.0/27.0
    def draw(self,win):
        #TODO move to update function
        if self.state == die:
            win.blit(playerDie, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
            return
        if self.particle.isClimb == True:
            self.changeState(climp)
        if moveSpeed == 0:
            self.changeState(idle)
        if self.direction == Right:
            if self.state == climp:

                win.blit(playerClimpRight, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))

            if self.state == shot:
                 self.animationCount +=1
                 win.blit(playerFireRight, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
                 if self.animationCount >5:
                    self.changeState(idle)
            if self.state==idle:
                 win.blit(playerIdleRight, (int(self.worldToCamera()[0]),int(self.worldToCamera()[1])))
            if self.state == running:
                if self.animationCount > 10:
                    self.animationCount =0
                self.animationCount +=1
                win.blit(playerRunRight[self.animationCount//6], (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        else:
            if self.state == climp:

                win.blit(playerClimpLeft, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
            if moveSpeed == 0:
                self.changeState(idle)
            if self.state == shot:
                 self.animationCount +=1
                 win.blit(playerFireLeft, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
                 if self.animationCount >5:
                    self.changeState(idle)
            if self.state==idle:
                 win.blit(playerIdleLeft, (int(self.worldToCamera()[0]),int(self.worldToCamera()[1])))
            if self.state == running:
                if self.animationCount > 10:
                    self.animationCount =0
                self.animationCount +=1
                win.blit(playerRunLeft[self.animationCount//6], (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))


class Ground(GameObject,object):
    def __init__(self, x, y, width, height, env):
        super(Ground, self).__init__(x, y, width, height, env)
        self.particle = BoxParticle(x,y,width,height)
        self.particle.static = True
        self.env.particles.append(self.particle)
        self.particle.parent = self
        self.name = "Ground"

    def kill(self):
        print("Kill")
        self.env.removeParticle(self.particle)
        self.tile.type = 0

class Box(GameObject,object):
    def __init__(self, x, y, width, height, env):
        super(Box, self).__init__(x, y, width, height, env)
        self.particle = BoxParticle(x,y,width,height)
        self.particle.static = False
        self.env.particles.append(self.particle)
        self.particle.parent = self
        self.name = "Box"
    def draw(self,win):
        win.blit(box, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
    def kill(self):
        print("Kill")
        self.env.removeParticle(self.particle)

class Water(GameObject,object):
    def __init__(self, x, y, width, height, env):
        super(Water, self).__init__(x, y, width, height, env)
        self.particle = BoxParticle(x,y,width,height)
        self.particle.static = True
        self.env.particles.append(self.particle)
        self.particle.parent = self
        self.name = "Water"

    def kill(self):
        print("Kill")
        #self.env.removeParticle(self.particle)
        #self.tile.type = 0

class Box(GameObject,object):
    def __init__(self, x, y, width, height, env):
        super(Box, self).__init__(x, y, width, height, env)
        self.particle = BoxParticle(x,y,width,height)
        self.particle.static = False
        self.env.particles.append(self.particle)
        self.particle.parent = self
        self.name = "Box"
    def draw(self,win):
        win.blit(box, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
    def kill(self):
        print("Kill")
        self.env.removeParticle(self.particle)

class Bullet(GameObject,object):
    def __init__(self, x, y, width, height, env,_from):
        super(Bullet, self).__init__(x, y, width, height, env)
        self.particle = BoxParticle(x,y,width,height)
        self.particle.static = False
        self.env.particles.append(self.particle)
        self.particle.isAffectByGravity = False
        self.timeToDie = 1
        self.countT = 0
        self.particle.parent = self
        self._from = _from
        self.name = "Bullet"
        self.particle.mass = 0.0001
        fireSound.play()
        if self.width > 2*bulletSize[0]:
            self.bullet = bossBullet
        else:
            self.bullet = bullet
    def setBullet(self,bullet):
        self.bullet = bullet
    def shot(self,angle):
        self.particle.accelerate(vector(angle,bulletSpeed))
    def hit(self,particle):
        if not particle == None:
            if self._from  != particle.parent.name :
                particle.parent.kill()

        self.kill()


    def kill(self):
        self.env.removeParticle(self.particle)

    def draw(self,win):
        win.blit(self.bullet, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))

    def update(self):
        # frame rate = 1/27
        self.countT += 1.0/27.0
        if self.countT > self.timeToDie:
            self.kill()


class Boom(GameObject,object):
    def __init__(self, x, y, width, height, env,_from):
        super(Boom, self).__init__(x, y, width, height, env)
        self.particle = BoxParticle(x,y,width,height)
        self.particle.static = False
        self.env.particles.append(self.particle)
        self.particle.isAffectByGravity = True
        self.timeToDie = 3
        self.countT = 0
        self.particle.parent = self
        self._from = _from
        self.name = "Boom"
        self.particle.mass = 0.0001
        self.timer  = 0

    def shot(self,angle):
        self.particle.accelerate(vector(angle,bulletSpeed))
    def hit(self,particle):
        if not particle == None:
            if self._from  != particle.parent.name :
                particle.parent.kill()

        p = Explosion(self.x,self.y-50,explosion,1,1,self.env)
        self.kill()


    def kill(self):
        self.env.removeParticle(self.particle)

    def draw(self,win):
        if self.timer >15:
            self.timer =15
        win.blit(boom[self.timer//4], (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))

    def update(self):
        # frame rate = 1/27
        self.timer+=1
        self.countT += 1.0/27.0
        if self.countT > self.timeToDie:
            self.kill()



class Enemy(GameObject, object):
    def __init__(self,x,y,width,height,player,env):
        super(Enemy,self).__init__(x,y,width,height,env)
        self.particle = BoxParticle(x, y, width, height)
        self.particle.static = False
        self.direction = Right
        self.env.particles.append(self.particle)
        self.particle.parent = self
        self.name = "Enemy"
        self.state = idle
        self.animationCount = 0
        self.shotCd = EnemyShotCd
        self.shotTimer = self.shotCd
        self.particle.isInAir = True
        self.deadTimer = 1
        self.player = player
    def kill(self):
        if self.state == die:
            return
        c = CoinTrigger(self.x,self.y,playerSize[0]/2,playerSize[0]/2,self.env)
        self.changeState(die)
        self.particle.static = False
        self.particle.height = self.particle.height/2
        #self.env.removeParticle(self.particle)

    def changeState(self, state):
        if self.state == state:
            return
        self.state = state
        self.animationCount = 0

    def moveLeft(self):
        self.direction = Left
        self.particle.moveLeft()
        self.changeState(running)

    def moveRight(self):
        self.changeState(running)
        self.direction = Right
        self.particle.moveRight()

    def moveUp(self):
        pass

    def moveDown(self):
        pass

    def jump(self):
        self.particle.jump()

    def shot(self):
        if not self.shotTimer <= 0:
            return
        self.shotTimer = self.shotCd
        self.changeState(shot)
        if self.direction == Right:
            offset = self.width + 5
        else:
            offset = -bulletOffset
        p = Bullet(self.particle.x + offset, self.particle.y + self.height / 2, bulletSize[0], bulletSize[1], self.env,self.name)
        p.shot(self.direction * math.pi / 2)

    def hit(self, particle):
        # print "hit "+ particle.parent.name
        pass

    def update(self):
        if self.state == die:
            self.deadTimer -= 1.0/27.0
            if self.deadTimer < 0:
                self.env.removeParticle(self.particle)
            return
        if self.shotTimer < 0:
            self.shotTimer = 0
        self.shotTimer -= 1.0 / 27.0

        if self.direction == Right:
            if self.player.x < self.x +enemyCensitiveSize[0] and self.player.x > self.x and self.player.y < self.y + enemyCensitiveSize[1] and self.player.y > self.y -self.width :
                self.shot()
        else:
            if self.player.x < self.x and self.player.x > self.x  - enemyCensitiveSize[0] and  self.player.y < self.y + \
                    enemyCensitiveSize[1] and self.player.y > self.y - self.width:
                self.shot()
    def draw(self, win):
        # TODO move to update function
        if self.particle.isClimb == True:
            self.changeState(climp)
        if moveSpeed == 0:
            self.changeState(idle)

        if self.state == die:
            win.blit(playerDie, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
            return

        if self.direction == Right:
            if self.state == climp:
                win.blit(playerClimpRight, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))

            if self.state == shot:
                self.animationCount += 1
                win.blit(playerFireRight, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
                if self.animationCount > 5:
                    self.changeState(idle)
            if self.state == idle:
                win.blit(playerIdleRight, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
            if self.state == running:
                if self.animationCount > 10:
                    self.animationCount = 0
                self.animationCount += 1
                win.blit(playerRunRight[self.animationCount // 6],
                         (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        else:
            if self.state == climp:
                win.blit(playerClimpLeft, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
            if moveSpeed == 0:
                self.changeState(idle)
            if self.state == shot:
                self.animationCount += 1
                win.blit(playerFireLeft, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
                if self.animationCount > 5:
                    self.changeState(idle)
            if self.state == idle:
                win.blit(playerIdleLeft, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
            if self.state == running:
                if self.animationCount > 10:
                    self.animationCount = 0
                self.animationCount += 1
                win.blit(playerRunLeft[self.animationCount // 6],
                         (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))


class Boss(Enemy, object):
    def __init__(self,x,y,width,height,player,env):
        super(Boss ,self).__init__(x,y,width,height,player,env)
        # self.particle = BoxParticle(x, y, width, height)




        self.hp = 10
        self.state = idle
        self.animationCount = 0
        self.shotCd = 10
        self.shotTimer = self.shotCd
        self.particle.isInAir = True
        self.particle.isAffectByGravity = False
        self.deadTimer = 5
        self.player = player
        self.moveChangeCount =10
        self.actionCount = 0

    def boom(self):
        if self.direction == Right:
            offset = 0
        else:
            offset = -100
        p = Boom(self.particle.x + self.width / 2 + offset, self.particle.y + self.height + 10,56,56, self.env, self.name)

    def shot(self):
        #self.shotTimer =6
        #self.changeState(shot)
        if self.direction == Right:
            offset = 0
        else:
            offset = -100
        p = Bullet(self.particle.x+ self.width/2 + offset, self.particle.y + self.height +10  , bulletSize[0]*3, bulletSize[1]*2,
                   self.env, self.name)
        p.shot(self.direction * math.pi / 2)

    def kill(self):

        if self.state == die:
            return
        if self.hp <=0:
            self.changeState(die)
            self.particle.isAffectByGravity = True
        self.hp -=1
        hitSound.play()

        #self.changeState(die)
        #self.particle.static = False
        #self.particle.height = self.particle.height / 2
        # self.env.removeParticle(self.particle)
    def update(self):

        self.animationCount +=1
        if self.animationCount > 7:
            self.animationCount = 0
        self.moveChangeCount -= 1.0/27.0
        if self.state == die:
            self.deadTimer -=1.0/27.0
            if self.deadTimer < 0 :
                self.env.removeParticle(self.particle)
        self.actionCount += 1
        if self.actionCount > 10*27:
            self.actionCount = 0
        if self.actionCount >0  and self.actionCount < 5*27:
            self.shotTimer -= 1.0/27.0
            if self.shotTimer < 0:
                self.shot()
                self.shotTimer = 0.5

        #TODO change shot timer to boom timer
        if self.actionCount >6*27 and self.actionCount <12*27:
            self.shotTimer -= 1.0 / 27.0
            if self.shotTimer < 0:
                self.boom()
                self.shotTimer = 0.5

        if self.moveChangeCount <0:
            self.moveChangeCount = 10

            if self.direction == Right:

                self.particle.speed =5
                self.particle.angle = -math.pi/2
                self.direction = Left
            else:
                self.particle.angle =math.pi / 2
                self.particle.speed =5
                self.direction = Right
        if self.state == die:
            self.deadTimer -= 1.0/27.0
            if self.deadTimer < 0:
                self.env.removeParticle(self.particle)
            return



    def draw(self, win):
        # TODO move to update function
        if self.direction == Right:
            win.blit(bossRight[self.animationCount//3], (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        else:
            win.blit(bossLeft[self.animationCount // 3], (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))


        # if self.particle.isClimb == True:
        #     self.changeState(climp)
        # if moveSpeed == 0:
        #     self.changeState(idle)
        #
        # if self.state == die:
        #     win.blit(playerDie, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        #     return
        #
        # if self.direction == Right:
        #     if self.state == climp:
        #         win.blit(playerClimpRight, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        #
        #     if self.state == shot:
        #         self.animationCount += 1
        #         win.blit(playerFireRight, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        #         if self.animationCount > 5:
        #             self.changeState(idle)
        #     if self.state == idle:
        #         win.blit(playerIdleRight, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        #     if self.state == running:
        #         if self.animationCount > 10:
        #             self.animationCount = 0
        #         self.animationCount += 1
        #         win.blit(playerRunRight[self.animationCount // 6],
        #                  (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        # else:
        #     if self.state == climp:
        #         win.blit(playerClimpLeft, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        #     if moveSpeed == 0:
        #         self.changeState(idle)
        #     if self.state == shot:
        #         self.animationCount += 1
        #         win.blit(playerFireLeft, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        #         if self.animationCount > 5:
        #             self.changeState(idle)
        #     if self.state == idle:
        #         win.blit(playerIdleLeft, (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
        #     if self.state == running:
        #         if self.animationCount > 10:
        #             self.animationCount = 0
        #         self.animationCount += 1
        #         win.blit(playerRunLeft[self.animationCount // 6],
        #                  (int(self.worldToCamera()[0]), int(self.worldToCamera()[1])))
