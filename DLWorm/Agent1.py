#Agent 1 (mechanical)

from Module import *
import math
import random

W1 = Worm(3, 3)
F1 = food(5,4)
F1.placement()
F2 = food(10, 10)
F2.placement()

#We need basic informations. Where the current location is, the wall is, and such as where the food is
#and which one is close etc.

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

  #And our little worm has to move for its objectives through dangerous things.
  #but first, he needs to see things.
  def worm_vision(self):

