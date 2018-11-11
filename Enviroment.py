from Particle import *
from Setup  import  *
from Map   import *
from params import  *
from Effect import  *
class Enviroment:
    def __init__(self,width,height):

        self.width = width
        self.height = height
        self.particles  = []
        self.effects =  []
        self.colour = (255,255,255)
        self.massOfAir =massOfAir
        self.elasticity = elasticity
        self.hasBoundaries = True
        self.acceleration = gravity
        self.particle_function1 = []
        self.particle_function2 = []
        self.collide = True
        self.function_dict = {
            'move': lambda p: p.move(),
            'drag': lambda p:p.experienceDrag(),
            'bounce': lambda p:p.bounce(self.width,self.height),
            'gravity': lambda p:p.experienceGravity(self.acceleration),
            'collide':lambda p1,p2: collide(p1,p2)
        }

    def setUpPlayer(self,player):
        self.player = player
    def addFunctions1(self,function_list):
        for func in function_list:
            f = self.function_dict.get(func,  None)
            if f:
                self.particle_function1.append(f)
            else:
                print
                "No such function: %s" % func

    def addFunctions2(self,function_list):
        for func in function_list:
            f = self.function_dict.get(func,  None)
            if f:
                self.particle_function2.append(f)
            else:
                print
                "No such function: %s" % func
    def addParticles(self, n=1, **kargs):
        ## circle
        # for i in range(2):
        #     r = kargs.get('size', random.randint(10, 20))
        #     mass = kargs.get('mass', random.randint(100, 10000))
        #     x = kargs.get('x', random.uniform(r, self.width - r))
        #     y = kargs.get('y', random.uniform(r, self.height - r))
        #     p = CircleParticle(x,y,r)
        #     p.speed = kargs.get('speed', random.random())/100
        #     p.angle = kargs.get('angle', random.uniform(0, math.pi * 2))
        #     p.colour = kargs.get('colour', (0, 0, 255))
        #     self.particles.append(p)

        for i in range(5):
            width = 3*kargs.get('size', random.randint(10, 20))
            height = 3*kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(100, 10000))
            if i == 1:
                p.static = True
            x = kargs.get('x', random.uniform(width, self.width - width))
            y = kargs.get('y', random.uniform(height, self.height - height))
            p = BoxParticle(x, y, width, height, mass)
            p.speed = kargs.get('speed', random.random()) / 100
            p.angle = kargs.get('angle', random.uniform(0, math.pi * 2))
            p.colour = kargs.get('colour', (0, 0, 255))

            self.particles.append(p)  #
    def update(self):
        i = 0
        d= 0
        for e in self.effects:
            e.update()
        collisionCount = 0
        for i,particle in enumerate(self.particles):

                if not particle.parent == None:
                    particle.parent.update()
                if particle.static:
                    continue

                for f in self.particle_function1:
                    f(particle)
                    #TODO: clean code
                for particle2 in self.particles:

                    if particle2 == particle:
                        continue

                    # if particle.static and particle2.static:
                    #     continue
                    # maxX =0
                    # maxY =0
                    # if particle.width > particle2.width:
                    #     maxX = particle.width
                    # else:
                    #     maxX = particle2.width
                    #
                    # if particle.height > particle2.height:
                    #     maxY = particle.height
                    # else:
                    #     maxY = particle2.height
                    if abs(particle.x - particle2.x) > 5*IMG_WIDTH:
                        continue
                    if abs(particle.y - particle2.y) >5*IMG_HEIGHT:
                        continue
                    collisionCount += 1
                    collide(particle, particle2)

                    # #for f in self.particle_function2:
                    #     if particle.static and particle2.static:
                    #         continue
                    #     elif particle.x > SCREEN_WIDTH or particle.x < 0:
                    #         continue
                    #     elif particle.y > SCREEN_HEIGHT or particle.y < 0:
                    #         continue
                    #     elif particle2.x > SCREEN_WIDTH or particle2.x < 0:
                    #         continue
                    #     elif particle2.y > SCREEN_HEIGHT or particle2.y < 0:
                    #         continue
                    #     else:
                    #
                    #         collide(particle,particle2)
        print(collisionCount)
        # print 'd =' + str(d)
        # print'i =' + str(i)

    def findParticles(self,x,y):
        for p in self.particles:
            if p.type == 1:
                if math.hypot(p.x - x, p.y - y) <= p.r:
                    return p
            else:
                if (x <p.getMaxX() and x > p.getMinX() and y> p.getMinY() and y < p.getMaxY()):
                    return p
        return None

    def removeParticle(self,particle):
        for i,p in enumerate(self.particles):
            if particle == p:
                del self.particles[i]
    def removeEffect(self,effect):
        for i,e in enumerate(self.effects):
            if effect == e:
                del self.effects[i]
    def draw(self):

        for p in self.particles:
            if p.static:
                continue
            if not p.parent == None:
                p.parent.draw(win)

        for e in self.effects:
            e.draw(win)

###########

