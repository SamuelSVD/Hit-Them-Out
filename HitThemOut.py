from physics import *
import pygame
from pygame.locals import *
import time

RADIUS = 10
offsetX = 250
offsetY = 250

images = ['Images/Main_Menu.png','Images/Background.png','Images/Paused.png','Images/HowToPlay.png','Images/LevelSelect.png','Images/blue.png','Images/red.png','Images/LevelSelect_BLACK.png','Images/Background.png']    
levels = [[(-100,0),(100,0)],
          [(-100,0),(0,0),(100,0)],
          [(0,0),(0,-100),(sqrt(3)*100,50),(-sqrt(3)*100,50)],
          [(-157,139),(-19,-151),(145,-102),(73,84)],
          [(-177,-11),(-3,-10),(-1,-40),(23,-19),(11,18),(-17,18)],
          [(-131,148),(-99,74),(-59,-10),(-179,-129),(29,-139),(99,-7),(115,120)],
          [(-191,84),(-87,82),(151,152),(157,76),(101,2),(-115,-2),(105,-92),(167,-146),(197,-89)],
          [(-180,-180),(-180,-90),(-180,0),(-180,90),(-180,180),(-90,180),(-90,-90),(0,0),(180,180),(90,90),(0,90),(0,180),(90,180),(-90,0),(-90,90)],
          [(-209,8),(-169,15),(-137,26),(-177,64),(-217,82),(-187,126),(-117,133),(-45,129),(-29,71),(-23,17),(13,-21),(69,-55),(117,-74),(131,-143),(181,-144),(173,-110),(211,-65),(195,-7),(139,-22)],
          [(-185,142),(-129,67),(83,43),(157,64),(167,5),(75,-37),(133,-83),(-95,-72),(-159,-57),(-147,-127)],
          [(-105,163),(-91,114),(-129,-78),(81,-76),(-21,-188),(43,84)],
          [(-181,23),(-93,-12),(-13,27),(51,-48),(5,-134),(105,17),(129,-116),(209,-106),(213,-28),(169,17),(41,69),(-1,149),(-107,163),(-125,100),(-179,127)]
          ]
levelClicks = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
MAIN_MENU = 0
GAME = 1
NEXT_LEVEL = 8
PAUSED = 2
HOW_TO_PLAY = 3
LEVEL_SELECT = 4
LEVEL_SELECT_BLACK = 7

BLUE = 5
RED = 6


#Complete
def loadImages():
    temp = []
    for name in images:
        temp.append(pygame.image.load(name))
    return temp

def drawBall(ballSet, screen, images):
    for ball in ballSet:
        pos = ball.getPosition()
        x = long(pos.getX())
        y = long(pos.getY())
        screen.blit(images[5+ball.getNumber()],(offsetX+x-int(RADIUS),offsetY+y-int(RADIUS)))
def calculateDelta(prevTime):
    #print (time.time()-prevTime)
    nTime = time.time()
    return nTime,(nTime-prevTime)

def updateObjects(ballSet,delta):
    for ball in ballSet:
        ball.update(delta)
        
def isColliding(ball1, ball2):
    pos1 = ball1.getPosition()
    pos2 = ball2.getPosition()
    #print ball1
    #print ball2
    dis = ((pos1.getX()-pos2.getX())**2+(pos1.getY()-pos2.getY())**2)**0.5
    return dis<2*RADIUS

def newLevel(i):
    ballSet = []
    for b in levels[i]:
        ballSet.append(Ball(1,MovingMass(1,Vector2D(b[0],b[1]),Vector2D(0,0),-2.5)))
    return ballSet

def calculateCollisions(ballSet, collisionTable):
#    print '========COLLISION======'
    newVelocities = []
    for l in collisionTable:
        newVelocities.append([])
#    print 'count A'
    for i in range(len(ballSet)):
        if ballSet[i].getVelocity().getMagnitude() > 0:
            balls = []
            indices = []
            hasStarted = False
#            print 'count B'
            for b in range(len(ballSet)):
                if collisionTable[i][b][1]:
                    if not hasStarted:
                        balls.append(ballSet[i])
                        indices.append(i)
                        hasStarted = True
#                    print 'count C'
                    balls.append(ballSet[b])
                    indices.append(b)
            velocities = collision(balls)
            #newVelocities[i].append(velocities)
            #print 'len Velocities',len(velocities)
            for b in range(len(indices)):
                #print 'b',b
                #print velocities[0]
                #print velocities[1]
                #print velocities[2]
                newVelocities[indices[b]].append(velocities[b])
#                print velocities[b]
    finalVelocities = [Vector2D(0,0)]*len(ballSet)
#    print 'count D'
    i = 0
    #print 'new Vs:',newVelocities
#    print '-------------------'
#    for vList in newVelocities:
#        for v in vList:
#            print 'Velocities:',v
#    print '-------------------'
    
    for i in range(len(newVelocities)):
        for b in range(len(newVelocities[i])):
            finalVelocities[i] = addVector2D(finalVelocities[i],newVelocities[i][b])
    
#    for v in finalVelocities:
#        print 'Final V:', v

    #if ball did not collide, finalVelocity[i].append(ballSet[i].getVelocity())
    for i in range(len(ballSet)):
        didCollide = False
        for j in range(len(ballSet)):
            if collisionTable[i][j][1]:
                didCollide = True
        #print i,'colided:',didCollide
        if not didCollide:
            finalVelocities[i] = ballSet[i].getVelocity()
    
    for i in range(len(ballSet)):
        #print 'before',ballSet[i].getVelocity().toString()
        #print finalVelocities[i].getMagnitude()
        ballSet[i].setVelocity(finalVelocities[i])
        #print 'after',ballSet[i].getVelocity().toString()
        

def printBall(ball):
    return [ball.getPosition().getX(),ball.getPosition().getY(),ball.getVelocity().getX(),ball.getVelocity().getY()]

def hasFinished(ballSet):
    for ball in ballSet:
        position = ball.getPosition()
        if (position.getX() + RADIUS > -250 and position.getX() - RADIUS < 250 and position.getY() + RADIUS > -250 and position.getY() - RADIUS < 250):
#            print ball
            return False
#    print 'all balls out of arena'
    return True

class Ball(MovingMass):
    def __init__(self, number, movingmass):
        self.number = number
        self.mass = movingmass.getMass()
        self.position = movingmass.getPosition()
        self.velocity = movingmass.getVelocity()
        self.acceleration = movingmass.getAcceleration()
    def __str__(self):
        return 'num:'+str(self.number)+'m:'+str(self.mass)+'\tp:'+self.position.toString()+'\tv:'+self.velocity.toString()+'\ta:'+str(self.acceleration)
    def setMass(self,mass):
        self.mass = mass
    def setPosition(self, Position2D):
        self.position = Position2D
    def setVelocity(self, Velocity2D):
        self.velocity = Velocity2D
    def setAcceleration(self, acceleration):
        self.acceleration = acceleration
    def getMass(self):
        return self.mass
    def getNumber(self):
        return self.number
    def getPosition(self):
        return self.position
    def getVelocity(self):
        return self.velocity
    def getAcceleration(self):
        return self.acceleration
    
def makeBallSet():
    ballSet = []
    #ball0 = MovingMass(1,Vector2D(-sqrt(2)*20, -20),Vector2D(sqrt(2)*10,10))

    #Checking colllisions
##    ball0 = Ball(1,MovingMass(1,Vector2D(0, 20),Vector2D(10,-2)))
##    ball1 = Ball(1,MovingMass(1,Vector2D(0, -20),Vector2D(10,2)))
##    ball2 = Ball(1,MovingMass(1,Vector2D(0, 100),Vector2D(10,0)))
##    ballSet.append(ball0)
##    ballSet.append(ball1)
##    ballSet.append(ball2)
    
    ball0 = Ball(0,MovingMass(1,Vector2D(-250, 0),Vector2D(00,0)))
    ballSet.append(ball0)
    
    ball1 = Ball(0,MovingMass(1,Vector2D(0, 0),Vector2D(0,0)))
    ballSet.append(ball1)
    x = 1.0
    y = 1.0
    
    ball2 = Ball(0,MovingMass(1,Vector2D(2*RADIUS*3**0.5/2+x, 2*RADIUS/2+y/2),Vector2D(0,0)))
    ballSet.append(ball2)
    ball3 = Ball(0,MovingMass(1,Vector2D(2*RADIUS*3**0.5/2+x, -2*RADIUS/2-y/2),Vector2D(0,0)))
    ballSet.append(ball3)
    
    ball4 = Ball(1,MovingMass(1,Vector2D(4*RADIUS*3**0.5/2+2*x, 20+y),Vector2D(0,0)))
    ballSet.append(ball4)
    ball5 = Ball(1,MovingMass(1,Vector2D(4*RADIUS*3**0.5/2+2*x, 0),Vector2D(0,0)))
    ballSet.append(ball5)
    ball6 = Ball(1,MovingMass(1,Vector2D(4*RADIUS*3**0.5/2+2*x, -20-y),Vector2D(0,0)))
    ballSet.append(ball6)

##    ball7 = MovingMass(1,Vector2D(6*RADIUS*3**0.5/2+3*x, 6*RADIUS/2+3*y/2),Vector2D(0,0))
##    ballSet.append(ball7)
##    ball8 = MovingMass(1,Vector2D(6*RADIUS*3**0.5/2+3*x, 2*RADIUS/2+y/2),Vector2D(0,0))
##    ballSet.append(ball8)
##    ball9 = MovingMass(1,Vector2D(6*RADIUS*3**0.5/2+3*x, -2*RADIUS/2-y/2),Vector2D(0,0))
##    ballSet.append(ball9)
##    ball10 = MovingMass(1,Vector2D(6*RADIUS*3**0.5/2+3*x, -6*RADIUS/2-3*y/2),Vector2D(0,0))
##    ballSet.append(ball10)
##
##    ball11 = MovingMass(1,Vector2D(8*RADIUS*3**0.5/2+4*x, 40+2*y),Vector2D(0,0))
##    ballSet.append(ball11)
##    ball12 = MovingMass(1,Vector2D(8*RADIUS*3**0.5/2+4*x, 20+y),Vector2D(0,0))
##    ballSet.append(ball12)
##    ball13 = MovingMass(1,Vector2D(8*RADIUS*3**0.5/2+4*x, 0),Vector2D(0,0))
##    ballSet.append(ball13)
##    ball14 = MovingMass(1,Vector2D(8*RADIUS*3**0.5/2+4*x, -20-y),Vector2D(0,0))
##    ballSet.append(ball14)
##    ball15 = MovingMass(1,Vector2D(8*RADIUS*3**0.5/2+4*x, -40-2*y),Vector2D(0,0))
##    ballSet.append(ball15)
##    
    
    for ball in ballSet:
        ball.setAcceleration(-2.5)
    return ballSet

def makeCollisionTable(size):
    x = []
    for i in range(size):
        s = []
        for b in range(size):
            s.append([(i,b),False])
        x.append(s)
    return x

def rewind(ballSet,delta):
    updateObjects(ballSet,-delta)

def printValues(ballSet):
    for b in ballSet:
        print b

def hit(ball, velocity):
    ball.setVelocity(velocity)

def main():
    #collisionDelay = [False]*10
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('Physics')
    running = True
    ballSet = makeBallSet()
    prevTime = time.time()
    delta = 0
    
    time.sleep(0.05)
    
    mouseHeld = False
    clickCount = 0
    ball = 0
    
    gameState = MAIN_MENU
    images = loadImages()
    currentLevel = 0
    levelsUnlocked = 0
    isPaused = False
    ballSet = newLevel(0)
    
    while(running):
        hasCollided = makeCollisionTable(len(ballSet))
        screen.fill((100,0,0))

#----------MAIN MENU----------#
        if (gameState == MAIN_MENU):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    print mousePos
                    if mousePos[0] > 32 and mousePos[0] <= 160 and mousePos[1] > 256 and mousePos[1] <= 308: 
                        gameState = LEVEL_SELECT
                    elif mousePos[0] > 32 and mousePos[0] <= 330 and mousePos[1] > 356 and mousePos[1] <= 409: 
                        gameState = HOW_TO_PLAY

            #Display
            screen.blit(images[MAIN_MENU],(0,0))



#-----------IN LEVEL SELECT---------#
        if (gameState == LEVEL_SELECT):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    #print mousePos
                    if mousePos[0] > 39 and mousePos[0] <= 239 and mousePos[1] > 397 and mousePos[1] <= 439: 
                        gameState = MAIN_MENU
                    elif mousePos[0] > 351 and mousePos[0] <= 445 and mousePos[1] > 394 and mousePos[1] <= 443: 
                        gameState = GAME
                    if mousePos[0] > 55 and mousePos[0] <= 437 and mousePos[1] > 170 and mousePos[1] <= 323:
                        mousePos = (((mousePos[0]-55)/63),(mousePos[1]-170)/60)
                        #print mousePos
                        #print 'level:',mousePos[0]+mousePos[1]*6
                        levelsUnlocked += 1
            screen.blit(images[LEVEL_SELECT],(0,0))
            for b in range(3):
                for i in range(6):
                    if levelsUnlocked < (i+b*6):
                        #print 'level:',i+b*6
                        screen.blit(images[LEVEL_SELECT_BLACK],(55+i*63,170+b*50),(55+i*63,170+b*50,63,50))


#-----------IN GAME----------#
        if (gameState == GAME):
            if not isPaused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN and not mouseHeld:
                        #print 'lol'
                        mousePos = pygame.mouse.get_pos()
                        #
                        #print '('+str(mousePos[0]-offsetX)+','+str(mousePos[1]-offsetY)+')'
                        #ballSet.append(Ball(1,MovingMass(1,Vector2D(mousePos[0]-offsetX,mousePos[1]-offsetY),Vector2D(0,0))))
                        #
                        
                        mouseHeld = True
                        if clickCount:
                            hit(ball,Vector2D((mousePos[0]-ball.getPosition().getX()-offsetX)/1,(mousePos[1]-ball.getPosition().getY()-offsetY)/1))
                            clickCount = 0
                        else:
                            for b in ballSet:
                                if ((b.getPosition().getX()+offsetX-mousePos[0])**2+(b.getPosition().getY()+offsetY-mousePos[1])**2)**0.5 < RADIUS:
                                    ball = b
                                    clickCount = 1
                                    
                                    break
                    else:
                        mouseHeld = False
    # handling keys
                keys = pygame.key.get_pressed()
                if keys[K_p] == True:
                    printValues(ballSet)
                    isPaused = not isPaused
                    
                if keys[K_r] == True:
                    ballSet = makeBallSet()
    #
                hasFinished(ballSet)
                
                prevTime, delta = calculateDelta(prevTime)
                delta = 0.025

                
                updateObjects(ballSet, delta)
                for i in range(len(ballSet)):
                    for b in range(i+1,len(ballSet)):
                        if isColliding(ballSet[i],ballSet[b]):
                            hasCollided[i][b][1] = True
                            hasCollided[b][i][1] = True
                            #for l in hasCollided:
                            #    print l
                collidedYe = False
                for i in range(len(hasCollided)):
                    for b in range(len(hasCollided)):
                        if hasCollided[i][b][1]:
                            #for b in ballSet:
                            #    print b.toString()
                            rewind(ballSet,delta)
                            calculateCollisions(ballSet, hasCollided)
        #                    for b in ballSet:
        #                        print b.toString()
                            #time.sleep(1)
                            collidedYe = True
                            #pygame.quit()
                            #return
                            break
                    if collidedYe:
                        break
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN and not mouseHeld:
                        #print 'lol'
                        mousePos = pygame.mouse.get_pos()
                        print mousePos
                        #if mousePos[0] > 25 and mousePos[0] <= 201 and mousePos[1] > 429 and mousePos[1] <= 466:
                        #    gameState = MAIN_MENU
                        mouseHeld = True
                    else:
                        mouseHeld = False

                keys = pygame.key.get_pressed()
                if keys[K_p] == True:
                    isPaused = not isPaused
                #if not keys[K_p] == True:
                #This is so it is not held.    
# Display
            screen.blit(images[GAME],(0,0))
            drawBall(ballSet,screen,images)
            if isPaused:
                screen.blit(images[PAUSED],(0,0))
#----------------IN NEXT LEVEL---------------#
        elif (gameState == NEXT_LEVEL):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
            screen.blit(images[NEXT_LEVEL],(0,0))
#-----------------HOW TO PLAY-----------------#
        elif (gameState == HOW_TO_PLAY):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    print mousePos
                    if mousePos[0] > 25 and mousePos[0] <= 201 and mousePos[1] > 429 and mousePos[1] <= 466:
                        gameState = MAIN_MENU
                    if mousePos[0] > 351 and mousePos[0] <= 431 and mousePos[1] > 433 and mousePos[1] <= 475:
                        gameState = GAME
                        
            #Display
            screen.blit(images[HOW_TO_PLAY],(0,0))
        
        pygame.display.flip()
        time.sleep(0.010)


main()
