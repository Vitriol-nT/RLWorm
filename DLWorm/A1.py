from Module import *
import math
import random

#Food1Position = [F1.pointxf, F1.pointyf]
#Food2position = [F2.pointxf, F2.pointyf]

class agent1:
  def __init__(self, W1, F1, F2):
    self.W1 = W1
    self.F1= F1
    self.F2 = F2
    self.Objective = 1
  
  #This guy needs to determine which one to eat.
  def calculateDistance(self):
    lengthF1 = math.sqrt((self.W1.pointx - self.F1.pointxf)**2 + (self.W1.pointy - self.F1.pointyf)**2)
    lengthF2 = math.sqrt((self.W1.pointx - self.F2.pointxf)**2 + (self.W1.pointy - self.F2.pointyf)**2)

    if (lengthF1 > lengthF2):
      self.Objective = 1
    elif (lengthF1 < lengthF2):
      self.Objective = 2
    else:
      self.Objective = random.randint(1, 2)

  #Following vector for food
  def setVector(self):
    if self.Objective == 1:
      self.directionVector = [(self.F1.pointxf - self.W1.pointx), (self.F1.pointyf - self.W1.pointy)]
      self.endPoint = [self.F1.pointxf, self.F1.pointyf]
    elif self.Objective == 2:
      self.directionVector = [(self.F2.pointxf - self.W1.pointx), (self.F2.pointyf - self.W1.pointy)]
      self.endPoint = [self.F2.pointxf, self.F2.pointyf]
  
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
      return math.exp(-0.5*z**2)

    #relative movement importance
    ti = math.abs(self.directionVector[0]) + math.abs(self.directionVector[1]) #Total Importance (ti)
    ix = self.directionVector[0]/ti #importance x
    iy = self.directionVector[1]/ti

    tendx = prob(1 - abs(ix*1))
    tendy = prob(1 - abs(iy*1))

    #SelfBody evasion
    readxp = []
    readxm = []
    readyp = []
    readym = []

    for i in 2:
      readxp.append(place[self.W1.pointx + (i+1), self.W1.pointy])
      readxm.append(place[self.W1.pointx - (i+1), self.W1.pointy])
    for j in 2:
      readyp.append(place[self.W1.pointx, self.W1.pointy + (j+1)])
      readym.append(place[self.W1.pointx, self.W1.pointy - (j+1)])
    #weld the possiblities together
    def essence():
      #body evasion
      if max(readxp) == 1:
        ix += 1
      elif max(readxm) == 1:
        ix -= 2
      elif max(readyp) == 1:
        iy = 1
      elif max(readym) == 1:
        iy -= 2
      else:
        pass
      try:
        #I will make it have tendency to move right
        quadrants = {
          (1, 1): [1, 4],
          (-1, -1): [2, 3],
          (1, -1): [2, 4],
          (-1, 1): [1, 3]
        }
        keyQ = (1 if ix >= 0 else -1, 1 if iy >= 0 else -1)
        outcomes = quadrants[keyQ]
        """ [u, d, l, r] = [1, 2, 3, 4] """
        ma.append(random.choices(outcomes, weights=[abs(iy), abs(ix)])[0])
      except:
        print("Error occured. Happens mostly because data went out of range. [0-19, 0-19].\n This will be counted as death")
        End = True
    #Wall evasion

    #recalling objective and setvector

    #polishing
    return self.movement_array

W1 = Worm(3, 3)
F1 = food(5,4)
F1.placement()
F2 = food(10, 10)
F2.placement()

Sanek = agent1(W1, F1, F2)

agent1.calculateDistance()
agent1.setVector()
agent1.action()

for i in len(agent1.movement_array):
  agent1.calculateDistance()
  agent1.setVector()
  agent1.action() 

print(agent1.movement_array)
