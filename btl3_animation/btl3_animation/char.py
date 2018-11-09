import os
import math
import pygame

KNIGHT_PATH = "asset" + os.sep + "Char" + os.sep + "knight"


class AnimationFrameData:
    def __init__(self, startFrame, numFrames):
        self.startFrame = 0
        self.numFrames = 0
        self.startFrame = startFrame
        self.numFrames = numFrames


class AnimationData:
    def __init__(self, images, frameInfo,scale):
        self.images = []
        self.facingLeftImages = []
        self.facingRightImages = []
        self.frameInfo = []
        self.images = [pygame.transform.scale(image,
                                            (int(image.get_rect().width * scale),
                                             int(image.get_rect().height * scale)))for image in images]
        self.frameInfo = frameInfo
        self.facingRightImages = self.images
        self.facingLeftImages = [pygame.transform.flip(image, True, False) for image in self.facingRightImages]


class Char(pygame.sprite.Sprite):

    def __init__(self):
        super(Char, self).__init__()
        self.SIZE_MULTIPLIER = 0.2
        self.animationData = self.__load_images(KNIGHT_PATH)
        self.frameTime = 0
        self.frameNum = 0
        self.animNum = self.IDEA
        self.vx = 0
        self.vy = 0
        self.isDead = True
        self.isFacingLeft = False
        self.changeAnimation(self.animNum)
        self.animFPS = float(24)
        self.rect = self.image.get_rect()
        self.set_position(100, 400)
        self.MOVEMENT_SPEED = 1
        self.JUMP_SPEED = 1


    def changeAnimation(self, num):
        self.animNum = num
        self.frameNum = 0
        self.animTime = 0.0
        animFrameData = self.animationData.frameInfo[self.animNum]
        imageNum = animFrameData.startFrame
        if self.isFacingLeft:
            self.image = self.animationData.facingLeftImages[imageNum]
        else:
            self.image = self.animationData.facingRightImages[imageNum]
    def __load_images(self, path):
        # empty images cache
        attack_images = []
        dead_images = []
        idea_images = []
        jump_images = []
        jump_attack_images = []
        run_images = []
        walk_images = []

        attack_images.append(pygame.image.load(path + os.sep + 'Attack (1).png'))
        attack_images.append(pygame.image.load(path + os.sep + 'Attack (2).png'))
        attack_images.append(pygame.image.load(path + os.sep + 'Attack (3).png'))
        attack_images.append(pygame.image.load(path + os.sep + 'Attack (4).png'))
        attack_images.append(pygame.image.load(path + os.sep + 'Attack (5).png'))
        attack_images.append(pygame.image.load(path + os.sep + 'Attack (6).png'))
        attack_images.append(pygame.image.load(path + os.sep + 'Attack (7).png'))
        attack_images.append(pygame.image.load(path + os.sep + 'Attack (8).png'))
        attack_images.append(pygame.image.load(path + os.sep + 'Attack (9).png'))
        attack_images.append(pygame.image.load(path + os.sep + 'Attack (10).png'))

        dead_images.append(pygame.image.load(path + os.sep + 'Dead (1).png'))
        dead_images.append(pygame.image.load(path + os.sep + 'Dead (2).png'))
        dead_images.append(pygame.image.load(path + os.sep + 'Dead (3).png'))
        dead_images.append(pygame.image.load(path + os.sep + 'Dead (4).png'))
        dead_images.append(pygame.image.load(path + os.sep + 'Dead (5).png'))
        dead_images.append(pygame.image.load(path + os.sep + 'Dead (6).png'))
        dead_images.append(pygame.image.load(path + os.sep + 'Dead (7).png'))
        dead_images.append(pygame.image.load(path + os.sep + 'Dead (8).png'))
        dead_images.append(pygame.image.load(path + os.sep + 'Dead (9).png'))
        dead_images.append(pygame.image.load(path + os.sep + 'Dead (10).png'))

        idea_images.append(pygame.image.load(path + os.sep + 'Idle (1).png'))
        idea_images.append(pygame.image.load(path + os.sep + 'Idle (2).png'))
        idea_images.append(pygame.image.load(path + os.sep + 'Idle (3).png'))
        idea_images.append(pygame.image.load(path + os.sep + 'Idle (4).png'))
        idea_images.append(pygame.image.load(path + os.sep + 'Idle (5).png'))
        idea_images.append(pygame.image.load(path + os.sep + 'Idle (6).png'))
        idea_images.append(pygame.image.load(path + os.sep + 'Idle (7).png'))
        idea_images.append(pygame.image.load(path + os.sep + 'Idle (8).png'))
        idea_images.append(pygame.image.load(path + os.sep + 'Idle (9).png'))
        idea_images.append(pygame.image.load(path + os.sep + 'Idle (10).png'))

        jump_images.append(pygame.image.load(path + os.sep + 'Jump (1).png'))
        jump_images.append(pygame.image.load(path + os.sep + 'Jump (2).png'))
        jump_images.append(pygame.image.load(path + os.sep + 'Jump (3).png'))
        jump_images.append(pygame.image.load(path + os.sep + 'Jump (4).png'))
        jump_images.append(pygame.image.load(path + os.sep + 'Jump (5).png'))
        jump_images.append(pygame.image.load(path + os.sep + 'Jump (6).png'))
        jump_images.append(pygame.image.load(path + os.sep + 'Jump (7).png'))
        jump_images.append(pygame.image.load(path + os.sep + 'Jump (8).png'))
        jump_images.append(pygame.image.load(path + os.sep + 'Jump (9).png'))
        jump_images.append(pygame.image.load(path + os.sep + 'Jump (10).png'))

        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (1).png'))
        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (2).png'))
        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (3).png'))
        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (4).png'))
        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (5).png'))
        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (6).png'))
        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (7).png'))
        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (8).png'))
        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (9).png'))
        jump_attack_images.append(pygame.image.load(path + os.sep + 'JumpAttack (10).png'))

        run_images.append(pygame.image.load(path + os.sep + 'Run (1).png'))
        run_images.append(pygame.image.load(path + os.sep + 'Run (2).png'))
        run_images.append(pygame.image.load(path + os.sep + 'Run (3).png'))
        run_images.append(pygame.image.load(path + os.sep + 'Run (4).png'))
        run_images.append(pygame.image.load(path + os.sep + 'Run (5).png'))
        run_images.append(pygame.image.load(path + os.sep + 'Run (6).png'))
        run_images.append(pygame.image.load(path + os.sep + 'Run (7).png'))
        run_images.append(pygame.image.load(path + os.sep + 'Run (8).png'))
        run_images.append(pygame.image.load(path + os.sep + 'Run (9).png'))
        run_images.append(pygame.image.load(path + os.sep + 'Run (10).png'))

        walk_images.append(pygame.image.load(path + os.sep + 'Walk (1).png'))
        walk_images.append(pygame.image.load(path + os.sep + 'Walk (2).png'))
        walk_images.append(pygame.image.load(path + os.sep + 'Walk (3).png'))
        walk_images.append(pygame.image.load(path + os.sep + 'Walk (4).png'))
        walk_images.append(pygame.image.load(path + os.sep + 'Walk (5).png'))
        walk_images.append(pygame.image.load(path + os.sep + 'Walk (6).png'))
        walk_images.append(pygame.image.load(path + os.sep + 'Walk (7).png'))
        walk_images.append(pygame.image.load(path + os.sep + 'Walk (8).png'))
        walk_images.append(pygame.image.load(path + os.sep + 'Walk (9).png'))
        walk_images.append(pygame.image.load(path + os.sep + 'Walk (10).png'))

        frame_info = []
        images = []
        sumFrames = 0

        self.IDEA = 0
        frame_info.append(AnimationFrameData(sumFrames, len(idea_images)))
        sumFrames += len(idea_images)
        images += idea_images

        self.ATTACK = 1
        frame_info.append(AnimationFrameData(sumFrames, len(attack_images)))
        sumFrames += len(attack_images)
        images += attack_images

        self.WALK = 2
        frame_info.append(AnimationFrameData(sumFrames, len(walk_images)))
        sumFrames += len(walk_images)
        images += walk_images

        self.RUN = 3
        frame_info.append(AnimationFrameData(sumFrames, len(run_images)))
        sumFrames += len(run_images)
        images += run_images

        self.JUMP = 4
        frame_info.append(AnimationFrameData(sumFrames, len(jump_images)))
        sumFrames += len(jump_images)
        images += jump_images

        self.JUMP_ATTACK = 5
        frame_info.append(AnimationFrameData(sumFrames, len(jump_attack_images)))
        sumFrames += len(jump_attack_images)
        images += jump_attack_images

        self.DEAD = 6
        frame_info.append(AnimationFrameData(sumFrames, len(dead_images)))
        sumFrames += len(dead_images)
        images += dead_images

        return AnimationData(images, frame_info,self.SIZE_MULTIPLIER)

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.vy += self.JUMP_SPEED
                self.changeAnimation(self.JUMP)
            elif event.key == pygame.K_RIGHT:
                self.isFacingLeft = False
                self.vx += self.MOVEMENT_SPEED
                if math.fabs(self.vx) < 100:
                    self.changeAnimation(self.WALK)
                else:
                    self.changeAnimation(self.RUN)
            elif event.key == pygame.K_LEFT:
                self.vx -= self.MOVEMENT_SPEED
                self.isFacingLeft = True
                if math.fabs(self.vx) < 10:
                    self.changeAnimation(self.WALK)
                else:
                    self.changeAnimation(self.RUN)
            elif event.key == pygame.K_SPACE:
                self.changeAnimation(self.ATTACK)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.vy = 0
                self.changeAnimation(self.JUMP_ATTACK)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                self.changeAnimation(self.IDEA)
                self.vx = 0

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, deltaTime):

        self.frameTime += deltaTime

        if self.frameTime > 1 / (self.animFPS):
            self.frameNum += self.frameTime * self.animFPS

        if self.frameNum >= self.animationData.frameInfo[self.animNum].numFrames:
            self.frameNum = int(self.frameNum % self.animationData.frameInfo[self.animNum].numFrames)

        imageNum = self.animationData.frameInfo[self.animNum].startFrame + self.frameNum
        if self.isFacingLeft:
            self.image = self.animationData.facingLeftImages[imageNum]
        else:
            self.image= self.animationData.facingRightImages[imageNum]

        self.frameTime = self.frameTime % (1 / self.animFPS)
        #s= v*dt
        self.rect.x += self.vx*deltaTime
        self.rect.y -= self.vy*deltaTime
