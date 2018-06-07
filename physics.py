#Created by: Samuel Vergara
# This physics took a lot to think about.... But it's done! It may be a little
# hard to follow, but just look back in any physics textbook and then you may
# be able to figure it out.

# Thanks to:
# Graham Todd for help guiding me in the correct direction with collisions
# near the beginning.

from math import *

class Vector2D:
    def __init__(self, x_coord, y_coord):
        self.x = float(x_coord)
        self.y = float(y_coord)
    def __str__(self):
        return 'x:'+str(self.x)+'\ty:'+str(self.y)
    def getType(self):
        return 'Vector2D'
    def setX(self, x_coord):
        self.x = float(x_coord)
    def xComponent(self):
        return Vector2D(self.x,0)
    def getX(self):
        return self.x
    def setY(self, y_coord):
        self.y = float(y_coord)
    def yComponent(self):
        return Vector2D(0,self.y)
    def getY(self):
        return self.y
    def getMagnitude(self):
        return (self.x**2+self.y**2)**0.5
    def setMagnitude(self,magnitude):
        m1 = self.getMagnitude()
        x1 = self.x
        y1 = self.y
        self.x = magnitude*x1/m1
        self.y = magnitude*y1/m1
    def toString(self):
        return 'x:'+str(self.x)+'\ty:'+str(self.y)

class MovingMass:
    def __init__(self,mass, Position2D = Vector2D(0,0), Velocity2D = Vector2D(0,0), acceleration = 0):
        self.velocity = Velocity2D
        self.position = Position2D
        self.mass = mass
        self.acceleration = acceleration
    def __str__(self):
        return 'm:'+str(self.mass)+'\tp:'+self.position.toString()+'\tv:'+self.velocity.toString()+'\ta:'+str(self.acceleration)
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
    def getPosition(self):
        return self.position
    def getVelocity(self):
        return self.velocity
    def getAcceleration(self):
        return self.acceleration
    def toString(self):
        return 'm:'+str(self.mass)+'\tp:'+self.position.toString()+'\tv:'+self.velocity.toString()+'\ta:'+str(self.acceleration)
    def update(self,delta):
        x = self.position.getX() + self.velocity.getX()*delta
        y = self.position.getY() + self.velocity.getY()*delta
        self.position = Vector2D(x,y)
        if self.velocity.getMagnitude() != 0:
            x = self.velocity.getX() + self.acceleration * self.velocity.getX()/self.velocity.getMagnitude()* delta
            y = self.velocity.getY() + self.acceleration * self.velocity.getY()/self.velocity.getMagnitude()* delta
            self.velocity = Vector2D(x,y)   
            if (self.velocity.getMagnitude()< 0.5):
                self.velocity = Vector2D(0,0)

#returns vectors of the new velocities
#THIS ONLY WORKS FOR EQUAL MASSED OBJECTS
def collision(ballSet):
    if len(ballSet) == 0:return
    pos = []
    for b in ballSet:
        pos.append(b.getPosition())
    directions = []
    for i in range(1,len(pos)):
        directions.append(Vector2D(pos[i].getX()-pos[0].getX(),pos[i].getY()-pos[0].getY()))

    v0 = ballSet[0].getVelocity()
    if v0 == 0:
        return
    energyTransfer = []
    for delta in directions:
        inside = abs(delta.getX()*v0.getX()+delta.getY()*v0.getY())/(delta.getMagnitude()*v0.getMagnitude())
        if inside > 1:
            inside = 1
        angle = acos(inside)
        energyTransfer.append(energyTransferred(angle))

    totEnergy = sum(energyTransfer)
    speeds = []
    velocities = []
    
    if totEnergy > 1:
        for energy in energyTransfer:
            speeds.append(sqrt((energy/totEnergy)*v0.getMagnitude()**2))
        velocities.append(Vector2D(0,0))
    else:
        for energy in energyTransfer:
            speeds.append(sqrt(energy*v0.getMagnitude()**2))
        v0x = v0.getX()
        v0y = v0.getY()
        for i in range(len(speeds)):
            v0x -= speeds[i]*directions[i].getX()/directions[i].getMagnitude()
            v0y -= speeds[i]*directions[i].getY()/directions[i].getMagnitude()
        velocities.append(Vector2D(v0x,v0y))
    for i in range(len(speeds)):
        velocities.append(Vector2D(speeds[i]*directions[i].getX()/directions[i].getMagnitude(),speeds[i]*directions[i].getY()/directions[i].getMagnitude()))

    return velocities
    
def energyTransferred(theta):
    if theta > pi/2: return 0
    else: return 1-(2.0/pi)*theta

def addVector2D(Vector2D_1, Vector2D_2):
    return Vector2D(Vector2D_1.getX()+Vector2D_2.getX(),Vector2D_1.getY()+Vector2D_2.getY())

def dotProduct(Vector1,Vector2):
    if (Vector1.getType() == Vector2.getType()):
        if Vector1.getType() == 'Vector2D':
            return Vector1.getX()*Vector2.getX()+Vector1.getY()*Vector2.getY()
        elif Vector1.getType() == 'Vector3D':
            return Vector1.getX()*Vector2.getX()+Vector1.getY()*Vector2.getY()+Vector1.getZ()*Vector2.getZ()
    else:
        raise Exception('Vector dimensions do not match')
GRAVITY = Vector2D(0,-9.80)
