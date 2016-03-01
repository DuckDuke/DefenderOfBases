##Created by Andrew (enjia2000@gmail.com)
##Defender of Bases 1.0 - 2/29/2016

import os, sys, pygame, random
from pygame.locals import *
#from math import pi

size = width, height = 280, 420
screen = pygame.display.set_mode(size, 0, 32)
Fullrect = Rect(0, 0, width,  height)
pygame.display.set_caption("Defender of Bases")
pygame.init()

###resources
fort = pygame.image.load('fort.png').convert_alpha()
background = pygame.image.load('background.png').convert_alpha()
score = 0 #global score
MaxCPUMissiles = 3
CPUMissiles = 0
MaxPlayerMissiles = 20
PlayerMissiles = 0
gameClock = pygame.time.Clock()

#screen.blit(fort, (15, 340))
#screen.blit(fort, (120, 320))
#screen.blit(fort, (215, 340))
#screen.blit(background, (0, 0))

#stationary object the player must defend.
class Fort:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x-5, y-5, 40, 15)

#CPU missiles.
cpuShots = []
class Missile:
    def __init__(self):
        global CPUMissiles
        CPUMissiles = CPUMissiles + 1
        self.color = (random.uniform(0, 255), random.uniform(0, 180), random.uniform(0, 180))
        self.startX = int(random.uniform(0, 280))
        self.destX = int(random.uniform(0, 280))
        self.lifetime = 100;
        self.destPos = [0, 375]
        self.startPos = [0, 0]
        self.destPos = (self.destX, int(self.destPos[1]))
        self.startPos = (self.startX, int(self.startPos[1]))
        self.lifespan = max( abs(int(self.destPos[0])-int(self.startPos[0])), abs(int(self.destPos[1])-int(self.startPos[1])) )
        self.stepx = float(int(self.destPos[0])-int(self.startPos[0]))/self.lifespan
        self.stepy = float(int(self.destPos[1])-int(self.startPos[1]))/self.lifespan
        self.pos = self.startPos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 16)
        cpuShots.append(self) #an array we can loop through when updating shots        
    def update(self):
        self.pos = (self.pos[0] + self.stepx, self.pos[1] + self.stepy)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 16)
        self.lifespan = self.lifespan - 1
        #print(self.lifespan)
        if self.lifespan <= 0:
            global CPUMissiles
            CPUMissiles = CPUMissiles - 1
            Explosion(self.destPos)
            cpuShots.remove(self)
        pygame.draw.line(screen, self.color, self.startPos, self.pos)


#the player's bullets.
playerShots = []
class PlayerShot:
    def __init__(self):
        global PlayerMissiles
        PlayerMissiles = PlayerMissiles + 1
        self.color = (random.uniform(0, 255), random.uniform(0, 180), random.uniform(0, 180))
        self.destPos = pygame.mouse.get_pos()
        self.gunSpots = ((60, 360), (220, 360))
        self.startPos = random.choice(self.gunSpots)
        self.startPos = random.choice(self.gunSpots)
        self.lifespan = max( abs(int(self.destPos[0])-int(self.startPos[0])), abs(int(self.destPos[1])-int(self.startPos[1])) )
        playerShots.append(self) #an array we can loop through when updating shots
        #print(self.lifespan)
        self.stepx = float(int(self.destPos[0])-int(self.startPos[0]))/self.lifespan
        self.stepy = float(int(self.destPos[1])-int(self.startPos[1]))/self.lifespan
        self.pos = self.startPos
    def update(self):
        #print(str(self.stepx)+ " " +str(self.stepy))
        self.pos = (self.pos[0] + self.stepx, self.pos[1] + self.stepy)
        #self.pos = self.pos + ((self.stepx), (self.stepy))
        #print(str(self.lifespan) + " moved " + str(self.pos))
        self.lifespan = self.lifespan - 1
        if self.lifespan == 0:
            global PlayerMissiles
            PlayerMissiles = PlayerMissiles - 1
            Explosion(self.destPos)
            playerShots.remove(self)
            #self.remove()
        pygame.draw.line(screen, self.color, self.startPos, self.pos)

#explosions.
explosions = []
class Explosion:
    def __init__(self, pos):
        self.color = (random.uniform(200, 255), random.uniform(0, 30), random.uniform(0, 30))
        self.pos = pos
        self.lifespan = 30
        explosions.append(self)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 16)
    def update(self):
        if self.lifespan <= 0:
            #print("removing self")
            explosions.remove(self)
        else:
            self.lifespan = self.lifespan - 1
            self.i = abs(int(self.lifespan-30))
            self.ir = abs(int(self.i)/2)
            #print(self.i)
            #print(str(self.pos[0]-int(self.i/2))+"," + str(self.pos[0]-int(self.i/2)))
            self.rect = pygame.Rect(self.pos[0]-self.ir, self.pos[1]-self.ir, self.i, self.i)
            pygame.draw.circle(screen, self.color, self.pos, self.i, 0)
            for x in cpuShots:
                if self.rect.colliderect(x.rect):
                    cpuShots.remove(x)
                    global CPUMissiles
                    CPUMissiles = CPUMissiles - 1
                    global score
                    score = score + 100
            for f in forts:
                if self.rect.colliderect(f.rect):
                    forts.remove(f)

            

#setup fort locations.
forts = []

def DropShadowText(text,  pos,  size):
    font = pygame.font.Font(None, size)
    fontimg1 = font.render(str(text), 1, (0, 0, 0))
    screen.blit(fontimg1, (pos[0], pos[1]))
    fontimg2 = font.render(str(text), 1 ,(255, 140, 140))
    screen.blit(fontimg2, (pos[0]-1, pos[1]-1))
    
def StartNewGame():
    global score
    score = 0 #global score

    o = Fort(fort,  15,  380)
    forts.append(o)
    o = Fort(fort,  120,  360)
    forts.append(o)
    o = Fort(fort,  215,  380)
    forts.append(o)
    
while 1:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            sys.exit(0)
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.display.quit()
            sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            if(PlayerMissiles < MaxPlayerMissiles):
                if (len(forts) > 0):
                    PlayerShot()
        elif event.type == KEYDOWN and event.key == K_F2:
            StartNewGame()
        
    screen.blit(background,  (0, 0))
    for f in forts:
        screen.blit(f.image,  (f.x,  f.y))
    for cs in cpuShots:
        cs.update()
    for ex in explosions:
        ex.update()
    for ps in playerShots:
        ps.update()
    MaxCPUMissiles = (int(score /300)+1)
    #print(score)
    
       
    DropShadowText(score,  (130, 392), 40)
    
    if (len(forts) > 0):
        if(CPUMissiles < MaxCPUMissiles):
            Missile()
        gameClock.tick(60) #advance the game one frame limited to 60fps
    else:
        DropShadowText("Game Over",  (80, 210), 28)
        DropShadowText("Press F2 to Start a new Game",  (20, 238), 24)
        #print("game over")

    pygame.display.update()
    pygame.display.flip()   
    
