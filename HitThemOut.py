# Created By: Samuel Vergara.
# Date Finished: 26 March 2014

# This game is simple. Get all the balls out of the screen while you still can!

#Thanks to: Graham Todd for helping me out with collisions and giving feedback
#           Derek Arts for giving some feedback with the game

from physics import *
import pygame
from pygame.locals import *
import time

RADIUS = 10
offsetX = 250
offsetY = 250

images = ['Images/Main_Menu.png','Images/Background.png','Images/Paused.png','Images/HowToPlay.png','Images/LevelSelect.png','Images/blue.png','Images/red.png','Images/LevelSelect_BLACK.png','Images/Next_Level.png','Images/GameFinished.png','Images/TryAgain.png','Images/LevelSelect_RED.png']
levels = [[(-100,0),(100,0)],
          [(-100,0),(0,0),(100,0)],
          [(0,0),(0,-150),(sqrt(3)*75,75),(-sqrt(3)*75,75)],
          [(-157,139),(-19,-151),(145,-102),(73,84)],

          [(-177,-11),(-3,-10),(-1,-40),(23,-19),(11,18),(-17,18)],
          [(-131,148),(-99,74),(-59,-10),(-179,-129),(29,-139),(99,-7),(115,120)],
          [(-191,84),(-87,82),(151,152),(157,76),(101,2),(-115,-2),(105,-92),(167,-146),(197,-89)],
          [(-180,-180),(-180,-90),(-180,0),(-180,90),(-180,180),(-90,180),(-90,-90),(0,0),(180,180),(90,90),(0,90),(0,180),(90,180),(-90,0),(-90,90)],

          [(-209,8),(-169,15),(-137,26),(-177,64),(-217,82),(-187,126),(-117,133),(-45,129),(-29,71),(-23,17),(13,-21),(69,-55),(117,-74),(131,-143),(181,-144),(173,-110),(211,-65),(195,-7),(139,-22)],
          [(-185,142),(-129,67),(83,43),(157,64),(167,5),(75,-37),(133,-83),(-95,-72),(-159,-57),(-147,-127)],
          [(-105,163),(-91,114),(-129,-78),(81,-76),(-21,-188),(43,84)],
          [(-181,23),(-93,-12),(-13,27),(51,-48),(5,-134),(105,17),(129,-116),(209,-106),(213,-28),(169,17),(41,69),(-1,149),(-107,163),(-125,100),(-179,127)],

          [(-192,-169),(-111,-96),(-11,-170),(54,-90),(164,-181),(182,-93),(164,51),(-90,34),(-8,43),(46,44),(-117,171),(51,154)],
          [(-197,-99),(-115,-152),(-59,-61),(96,-58),(207,5),(106,37),(-27,45),(-82,137),(-163,213),(-21,205),(112,138),(217,161)],
          [(-146,-200),(-199,-118),(-73,-79),(18,-158),(59,-48),(119,17),(209,16),(208,-48),(-44,42),(33,62),(49,158),(-85,133),(158,200),(81,240),(-187,151),(-218,55),],
          [(-228,30),(-66,25),(1,-59),(89,-34),(47,22),(134,-105),(189,-135),(193,-203),(-60,-139),(85,115),(182,182)],

          [(-203,201),(-183,144),(-138,158),(-153,188),(-167,-59),(-146,-170),(-13,-107),(-52,4),(-4,102),(86,129),(158,92),(153,-32),(197,-134)],
          [(0,-141), (10,-123), (-10,-123), (0,-106), (20,-106), (-20,-106), (10,-89), (30,-89), (-10,-89), (-30,-89), (0,-72), (20,-72), (-20,-72), (40,-72), (-40,-72), (10,-55), (30,-55), (50,-55), (-10,-55), (-30,-55), (-50,-55),(-60,-39), (-50,-21), (-70,-21), (-60,-4), (-40,-4), (-80,-4), (-50,13), (-30,13), (-70,13), (-90,13), (-60,30), (-40,30), (-80,30), (-20,30), (-100,30), (-50,47), (-30,47), (-10,47), (-70,47), (-90,47), (-110,47), (60,-39), (70,-21), (50,-21), (60,-4), (80,-4), (40,-4), (70,13), (90,13), (50,13), (30,13), (60,30), (80,30), (40,30), (100,30), (20,30), (70,47), (90,47), (110,47), (50,47), (30,47), (10,47)]]
clicksAllowed = [1, 2, 2, 2, 2, 3, 4, 6, 6, 5, 3, 5, 5, 5, 7, 5, 5, 1]


levels = [[(-100, 0), (100, 0)] ,
          [(-100, 0), (0, 0), (100, 0)] ,
          [(0, 0), (0, -150), (129.9038105676658, 75), (-129.9038105676658, 75)] ,
          [(-157, 139), (-19, -151), (145, -102), (73, 84)] ,
          [(-177, -11), (-3, -10), (-1, -40), (23, -19), (11, 18), (-17, 18)] ,
          [(-131, 148), (-99, 74), (-59, -10), (-179, -129), (29, -139), (99, -7), (115, 120)] ,
          [(-105, 163), (-91, 114), (-129, -78), (81, -76), (-21, -188), (43, 84)] ,
          [(-191, 84), (-87, 82), (151, 152), (157, 76), (101, 2), (-115, -2), (105, -92), (167, -146), (197, -89)] ,
          [(-185, 142), (-129, 67), (83, 43), (157, 64), (167, 5), (75, -37), (133, -83), (-95, -72), (-159, -57), (-147, -127)] ,
          [(-228, 30), (-66, 25), (1, -59), (89, -34), (47, 22), (134, -105), (189, -135), (193, -203), (-60, -139), (85, 115), (182, 182)] ,
          [(-203, 201), (-183, 144), (-138, 158), (-153, 188), (-167, -59), (-146, -170), (-13, -107), (-52, 4), (-4, 102), (86, 129), (158, 92), (153, -32), (197, -134)] ,
          [(-181, 23), (-93, -12), (-13, 27), (51, -48), (5, -134), (105, 17), (129, -116), (209, -106), (213, -28), (169, 17), (41, 69), (-1, 149), (-107, 163), (-125, 100), (-179, 127)] ,
          [(-192, -169), (-111, -96), (-11, -170), (54, -90), (164, -181), (182, -93), (164, 51), (-90, 34), (-8, 43), (46, 44), (-117, 171), (51, 154)] ,
          [(-197, -99), (-115, -152), (-59, -61), (96, -58), (207, 5), (106, 37), (-27, 45), (-82, 137), (-163, 213), (-21, 205), (112, 138), (217, 161)] ,
          [(-180, -180), (-180, -90), (-180, 0), (-180, 90), (-180, 180), (-90, 180), (-90, -90), (0, 0), (180, 180), (90, 90), (0, 90), (0, 180), (90, 180), (-90, 0), (-90, 90)] ,
          [(-209, 8), (-169, 15), (-137, 26), (-177, 64), (-217, 82), (-187, 126), (-117, 133), (-45, 129), (-29, 71), (-23, 17), (13, -21), (69, -55), (117, -74), (131, -143), (181, -144), (173, -110), (211, -65), (195, -7), (139, -22)] ,
          [(-146, -200), (-199, -118), (-73, -79), (18, -158), (59, -48), (119, 17), (209, 16), (208, -48), (-44, 42), (33, 62), (49, 158), (-85, 133), (158, 200), (81, 240), (-187, 151), (-218, 55)] ,
          [(0, -141), (10, -123), (-10, -123), (0, -106), (20, -106), (-20, -106), (10, -89), (30, -89), (-10, -89), (-30, -89), (0, -72), (20, -72), (-20, -72), (40, -72), (-40, -72), (10, -55), (30, -55), (50, -55), (-10, -55), (-30, -55), (-50, -55), (-60, -39), (-50, -21), (-70, -21), (-60, -4), (-40, -4), (-80, -4), (-50, 13), (-30, 13), (-70, 13), (-90, 13), (-60, 30), (-40, 30), (-80, 30), (-20, 30), (-100, 30), (-50, 47), (-30, 47), (-10, 47), (-70, 47), (-90, 47), (-110, 47), (60, -39), (70, -21), (50, -21), (60, -4), (80, -4), (40, -4), (70, 13), (90, 13), (50, 13), (30, 13), (60, 30), (80, 30), (40, 30), (100, 30), (20, 30), (70, 47), (90, 47), (110, 47), (50, 47), (30, 47), (10, 47)]]

clicksAllowed = [1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 7, 1]

MAIN_MENU = 0
GAME = 1
NEXT_LEVEL = 8
PAUSED = 2
HOW_TO_PLAY = 3
LEVEL_SELECT = 4
LEVEL_SELECT_BLACK = 7
LEVEL_SELECT_RED = 11
GAME_FINISHED = 9
TRY_AGAIN = 10

BLUE = 5
RED = 6

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
    nTime = time.time()
    return nTime,(nTime-prevTime)

def updateObjects(ballSet,delta):
    for ball in ballSet:
        ball.update(delta)
        
def isColliding(ball1, ball2):
    pos1 = ball1.getPosition()
    pos2 = ball2.getPosition()
    dis = ((pos1.getX()-pos2.getX())**2+(pos1.getY()-pos2.getY())**2)**0.5
    return dis<2*RADIUS

def newLevel(i):
    ballSet = []
    for b in levels[i]:
        ballSet.append(Ball(1,MovingMass(1,Vector2D(b[0],b[1]),Vector2D(0,0),-2.5)))
    return ballSet

def calculateCollisions(ballSet, collisionTable):
    newVelocities = []
    for l in collisionTable:
        newVelocities.append([])
    for i in range(len(ballSet)):
        if ballSet[i].getVelocity().getMagnitude() > 0:
            balls = []
            indices = []
            hasStarted = False
            for b in range(len(ballSet)):
                if collisionTable[i][b][1]:
                    if not hasStarted:
                        balls.append(ballSet[i])
                        indices.append(i)
                        hasStarted = True
                    balls.append(ballSet[b])
                    indices.append(b)
            velocities = collision(balls)
            for b in range(len(indices)):
                newVelocities[indices[b]].append(velocities[b])
    finalVelocities = [Vector2D(0,0)]*len(ballSet)
    i = 0

    for i in range(len(newVelocities)):
        for b in range(len(newVelocities[i])):
            finalVelocities[i] = addVector2D(finalVelocities[i],newVelocities[i][b])
    
    for i in range(len(ballSet)):
        didCollide = False
        for j in range(len(ballSet)):
            if collisionTable[i][j][1]:
                didCollide = True
        if not didCollide:
            finalVelocities[i] = ballSet[i].getVelocity()
    
    for i in range(len(ballSet)):
        ballSet[i].setVelocity(finalVelocities[i])
        

def printBall(ball):
    return [ball.getPosition().getX(),ball.getPosition().getY(),ball.getVelocity().getX(),ball.getVelocity().getY()]

def hasFinished(ballSet):
    for ball in ballSet:
        position = ball.getPosition()
        if (position.getX() + RADIUS > -250 and position.getX() - RADIUS < 250 and position.getY() + RADIUS > -250 and position.getY() - RADIUS < 250):
            return False
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
    pygame.display.set_icon(pygame.image.load("Images/img.png"))
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('Hit Them Out!')
        
    images = loadImages()
    
    prevTime = time.time()
    delta = 0
    
    time.sleep(0.05)
    
    mouseHeld = False
    pisHeld = False
    clickCount = 0
    currentClicks = 0
    ball = 0
    
    gameState = MAIN_MENU
    currentLevel = 0
    levelsUnlocked = 0
    ballSet = []
    isPaused = False
    
    nextLevel = time.time()
    endTimer = time.time()
    running = True

    pygame.font.init()
    font = pygame.font.SysFont('lucida', 40, True, False)
    
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
                    if mousePos[0] > 32 and mousePos[0] <= 160 and mousePos[1] > 256 and mousePos[1] <= 308: 
                        gameState = LEVEL_SELECT
                    elif mousePos[0] > 32 and mousePos[0] <= 330 and mousePos[1] > 356 and mousePos[1] <= 409: 
                        gameState = HOW_TO_PLAY

# Display
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
                    if mousePos[0] > 39 and mousePos[0] <= 239 and mousePos[1] > 397 and mousePos[1] <= 439: 
                        gameState = MAIN_MENU
                    elif mousePos[0] > 351 and mousePos[0] <= 445 and mousePos[1] > 394 and mousePos[1] <= 443: 
                        gameState = GAME
                        ballSet = newLevel(currentLevel)
                        hasCollided = makeCollisionTable(len(ballSet))
                        currentClicks = 0
                    if mousePos[0] > 55 and mousePos[0] <= 437 and mousePos[1] > 170 and mousePos[1] <= 323:
                        mousePos = (((mousePos[0]-55)/63),(mousePos[1]-170)/60)
                        if (mousePos[0]+mousePos[1]*6 <= levelsUnlocked):
                            currentLevel = mousePos[0]+mousePos[1]*6

# Display
            screen.blit(images[LEVEL_SELECT],(0,0))
            for b in range(3):
                for i in range(6):
                    if levelsUnlocked < (i+b*6):
                        screen.blit(images[LEVEL_SELECT_BLACK],(55+i*63,170+b*50),(55+i*63,170+b*50,63,50))
            screen.blit(images[LEVEL_SELECT_RED],(55+currentLevel%6*63,170+currentLevel/6*50),(55+currentLevel%6*63,170+currentLevel/6*50,63,50))


#-----------IN GAME----------#
        if (gameState == GAME):
            if not isPaused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN and not mouseHeld:
                        mousePos = pygame.mouse.get_pos()
                        if clickCount:
                            if currentClicks < clicksAllowed[currentLevel]:
                                if not (((ball.getPosition().getX()+offsetX-mousePos[0])**2+(ball.getPosition().getY()+offsetY-mousePos[1])**2)**0.5 < RADIUS):
                                    hit(ball,Vector2D((mousePos[0]-ball.getPosition().getX()-offsetX)/1,(mousePos[1]-ball.getPosition().getY()-offsetY)/1))
                                    clickCount = 0
                                    ball = 0
                                    currentClicks += 1
                            if currentClicks == clicksAllowed[currentLevel]:
                                endTimer = time.time()+10
                                
                        else:
                            if currentClicks < clicksAllowed[currentLevel]:
                                for b in ballSet:
                                    if ((b.getPosition().getX()+offsetX-mousePos[0])**2+(b.getPosition().getY()+offsetY-mousePos[1])**2)**0.5 < RADIUS:
                                        ball = b
                                        clickCount = 1
                                        break
                
# Handling keys
                keys = pygame.key.get_pressed()
                if (keys[K_p] == True or keys[K_ESCAPE] == True)and not pisHeld:
                    isPaused = not isPaused
                    pisHeld = True
                if keys[K_p] == False and keys[K_ESCAPE] == False:
                    pisHeld = False
                if keys[K_r] == True:
                    ballSet = newLevel(currentLevel)
                    currentClicks = 0
                    hasCollided = makeCollisionTable(len(ballSet))
        
                
                prevTime, delta = calculateDelta(prevTime)
                if delta > 0.05:
                    delta = 0.05
                
                updateObjects(ballSet, delta)
                for i in range(len(ballSet)):
                    for b in range(i+1,len(ballSet)):
                        if isColliding(ballSet[i],ballSet[b]) and b != i:
                            hasCollided[i][b][1] = True
                            hasCollided[b][i][1] = True
                collidedYe = False
                for i in range(len(hasCollided)):
                    for b in range(len(hasCollided)):
                        if hasCollided[i][b][1]:
                            rewind(ballSet,delta)
                            calculateCollisions(ballSet, hasCollided)
                            collidedYe = True
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
                        mousePos = pygame.mouse.get_pos()
                        if mousePos[0] > 145 and mousePos[0] <= 357 and mousePos[1] > 210 and mousePos[1] <= 250:
                            isPaused = False
                        if mousePos[0] > 145 and mousePos[0] <= 357 and mousePos[1] > 258 and mousePos[1] <= 299:
                            ballSet = newLevel(currentLevel)
                            currentClicks = 0
                            hasCollided = makeCollisionTable(len(ballSet))
                            isPaused = False
                        if mousePos[0] > 145 and mousePos[0] <= 357 and mousePos[1] > 305 and mousePos[1] <= 337:
                            gameState = LEVEL_SELECT
                            isPaused = False
                        if mousePos[0] > 145 and mousePos[0] <= 357 and mousePos[1] > 348 and mousePos[1] <= 381:
                            gameState = MAIN_MENU
                            isPaused = False

                keys = pygame.key.get_pressed()
                if (keys[K_p] == True or keys[K_ESCAPE] == True)and not pisHeld:
                    isPaused = not isPaused
                    pisHeld = True
                if keys[K_p] == False and keys[K_ESCAPE] == False:
                    pisHeld = False

# Display
            screen.blit(images[GAME],(0,0))
            drawBall(ballSet,screen,images)
            screen.blit(font.render(str(clicksAllowed[currentLevel]-currentClicks),1,(255,255,255,1)),(400,20))
            if isPaused:
                screen.blit(images[PAUSED],(0,0))

# Other    
            if currentClicks >= clicksAllowed[currentLevel]:
                # if balls still in an none moving TRY_AGAIN
                stillMoving = False
                for ball in ballSet:
                    position = ball.getPosition()
                    if (position.getX() + RADIUS > -250 and position.getX() - RADIUS < 250 and position.getY() + RADIUS > -250 and position.getY() - RADIUS < 250):
                        if ball.getVelocity().getMagnitude() > 0:
                            stillMoving = True
                if not stillMoving:
                    gameState = TRY_AGAIN
                    endTimer = time.time()+1
                if endTimer - time.time() < 0:
                    gameState = TRY_AGAIN
                    endTimer = time.time()+1
            
            if hasFinished(ballSet):
                currentLevel += 1
                if currentLevel > levelsUnlocked:
                    levelsUnlocked += 1
                gameState = NEXT_LEVEL
                if currentLevel == 18:
                    currentLevel = 0
                    gameState = GAME_FINISHED
                nextLevel = time.time() +2
                ballSet = newLevel(currentLevel)
                currentClicks = 0
                hasCollided = makeCollisionTable(len(ballSet))
        
            
#----------------IN NEXT LEVEL---------------#
        elif (gameState == NEXT_LEVEL):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return

            if nextLevel-time.time() < 0:
                gameState = GAME
                currentClicks = 0
                hasCollided = makeCollisionTable(len(ballSet))
        

# Display
            x = (500 * ((3-(nextLevel-time.time()))/3.0))
            if x  > 500:
                x = 500
            screen.blit(images[GAME],(0,0))
            screen.blit(images[NEXT_LEVEL],(0,0),(0,0,x,500))

#----------------IN TRY AGAIN-----------------#
        elif (gameState == TRY_AGAIN):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return

            if endTimer-time.time() < 0:
                gameState = GAME
                currentClicks = 0
                ballSet = newLevel(currentLevel)
                hasCollided = makeCollisionTable(len(ballSet))
                isPaused = False
# Display
            screen.blit(images[TRY_AGAIN],(0,0))


#-----------------HOW TO PLAY-----------------#
        elif (gameState == HOW_TO_PLAY):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if mousePos[0] > 25 and mousePos[0] <= 201 and mousePos[1] > 429 and mousePos[1] <= 466:
                        gameState = MAIN_MENU
                    if mousePos[0] > 351 and mousePos[0] <= 431 and mousePos[1] > 433 and mousePos[1] <= 475:
                        gameState = LEVEL_SELECT
                        
# Display
            screen.blit(images[HOW_TO_PLAY],(0,0))

#-----------------GAME FINISHED-----------------#
        elif (gameState == GAME_FINISHED):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if mousePos[0] > 138 and mousePos[0] <= 347 and mousePos[1] > 395 and mousePos[1] <= 429:
                        gameState = MAIN_MENU
# Display
            screen.blit(images[GAME_FINISHED],(0,0))

        
        pygame.display.flip()
        time.sleep(0.010)


main()
