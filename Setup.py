import  math
import pygame
class vector:
    def __init__(self,angle,length):
        self.angle = angle
        self.length = length


updateRate = 1.0/60
drag =1
elasticity = 0.99
massOfAir = 0.2
jumpVector =vector(0,20)
moveSpeed = 5
boxType =2
gravity = vector(math.pi, 1)
defaultSpeed = 1
bulletSize = (20,20)
playerStartPosition = (800,100)
playerSize = (56,56)
enemyCensitiveSize=(300,200)
PlayerShotCd =  0.1
EnemyShotCd = 1
boxSize = (40,40)
groundSize = (40,40)
Right = 1
Left = -1
bulletSpeed = 20
bulletOffset = 20
#character state
running = 1
die = -1
idle = 0
shot = 2
jump =3
climp = 4
up = 5
down = 6
airControllLoss =  0.1

