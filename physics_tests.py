from physics import *
import pygame
from pygame.locals import *
import time

RADIUS = 10
offsetX = 250
offsetY = 250

def drawBall(ballSet, screen):
    for ball in ballSet:
        pos = ball.getPosition()
        x = long(pos.getX())
        y = long(pos.getY())
        pygame.draw.circle(screen, (100,100,100),(offsetX+x,offsetY+y),int(RADIUS))

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
        if not didCollide:
            finalVelocities[i] = ballSet[i].getVelocity()
    
    for i in range(len(ballSet)):
        #print 'before',ballSet[i].getVelocity().toString()
        #print finalVelocities[i].getMagnitude()
        ballSet[i].setVelocity(finalVelocities[i])
        #print 'after',ballSet[i].getVelocity().toString()
        

def printBall(ball):
    return [ball.getPosition().getX(),ball.getPosition().getY(),ball.getVelocity().getX(),ball.getVelocity().getY()]

def makeBallSet():
    ballSet = []
    #ball0 = MovingMass(1,Vector2D(-sqrt(2)*20, -20),Vector2D(sqrt(2)*10,10))
    ball0 = MovingMass(1,Vector2D(-250, 0),Vector2D(00,0))
    ballSet.append(ball0)
    
    ball1 = MovingMass(1,Vector2D(0, 0),Vector2D(0,0))
    ballSet.append(ball1)
    x = 1.0
    y = 1.0
    
    ball2 = MovingMass(1,Vector2D(2*RADIUS*3**0.5/2+x, 2*RADIUS/2+y/2),Vector2D(0,0))
    ballSet.append(ball2)
    ball3 = MovingMass(1,Vector2D(2*RADIUS*3**0.5/2+x, -2*RADIUS/2-y/2),Vector2D(0,0))
    ballSet.append(ball3)
    
    ball4 = MovingMass(1,Vector2D(4*RADIUS*3**0.5/2+2*x, 20+y),Vector2D(0,0))
    ballSet.append(ball4)
    ball5 = MovingMass(1,Vector2D(4*RADIUS*3**0.5/2+2*x, 0),Vector2D(0,0))
    ballSet.append(ball5)
    ball6 = MovingMass(1,Vector2D(4*RADIUS*3**0.5/2+2*x, -20-y),Vector2D(0,0))
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
    
    
    for ball in ballSet:
        ball.setAcceleration(0)#-2.5)
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
    while(running):
        hasCollided = makeCollisionTable(len(ballSet))
        screen.fill((100,0,0))
        prevTime, delta = calculateDelta(prevTime)
        delta = 0.025
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and not mouseHeld:
                #print 'lol'
                mousePos = pygame.mouse.get_pos()
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
            
        updateObjects(ballSet, delta)
        for i in range(len(ballSet)):
            for b in range(i+1,len(ballSet)):
                if isColliding(ballSet[i],ballSet[b]):
                    hasCollided[i][b][1] = True
                    hasCollided[b][i][1] = True
                    for l in hasCollided:
                        print l
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

        #handling keys
        keys = pygame.key.get_pressed()
        if keys[K_p] == True:
            printValues(ballSet)
        if keys[K_r] == True:
            ballSet = makeBallSet()
        #
        
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,0,350,2*offsetY))
        drawBall(ballSet,screen)
        
        pygame.display.flip()
        time.sleep(0.010)


main()
