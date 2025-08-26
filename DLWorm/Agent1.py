from Module import *
import math
import random

W1 = Worm(3, 3)
F1 = food(5,4)
F1.placement()
F2 = food(10, 10)
F2.placement()

#Food1Position = [F1.pointxf, F1.pointyf]
#Food2position = [F2.pointxf, F2.pointyf]

class agent1:
  def __init__(self):
    self.pointx = W1.pointx
    self.pointy = W1.pointy
    self.Objective = 1
  
  #This guy needs to determine which one to eat.
  def calculateDistance(self):
    lengthF1 = math.sqrt((self.pointx - F1.pointxf)**2 + (self.pointy - F1.pointyf)**2)
    lengthF2 = math.sqrt((self.pointx - F2.pointxf)**2 + (self.pointy - F2.pointyf)**2)

    if (lengthF1 > lengthF2):
      self.Objective = 1
    elif (lengthF1 < lengthF2):
      self.Objective = 2
    else:
      self.Objective = random.randint(1, 2)

  #Following vector for food
  def setVector(self):
    if self.Objective == 1:
      directionVector = [(F1.pointxf - self.pointx), (F1.pointyf - self.pointy)]
      endPoint = [F1.pointxf, F1.pointyf]
    elif self.Objective == 2:
      directionVector = [(F2.pointxf - self.pointx), (F2.pointyf - self.pointy)]
      endPoint = [F2.pointxf, F2.pointyf]
  
  #Follow the vector and evade the collision with its body
  def action():
    self.movement_array = []
    ma = self.movement_array
    #its movement behavior should match the vector
    #we need to define numbers to match string direction styles.
    """ [u, d, l, r] = [1, 2, 3, 4] """
    #with the set of moves.
    #probalistic approach
    def prob(z):
      math.exp(-0.5*z**2)

    #relative movement importance
    ti = math.abs(directionVector[0]) + math.abs(directionVector[1]) #Total Importance (ti)
    ix = directionVector[0]/ti #importance x
    iy = directionVector[1]/ti

    tendx = prob(3 - math.abs(ix*3))
    tendy = prob(3 - math.abs(iy*3))
    if ix > 0 and iy > 0:
      if tendx > tendy:
        ma.append(1)
      elif tendx < tendy:
        ma.append(2)
      elif tendx == tendx:
        ma.append(4)
    elif ix < 0 and iy < 0:
      pass
      
