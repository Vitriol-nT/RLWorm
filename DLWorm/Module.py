#with time library exported when used in code, make the delay and forever loop to be on the course
#COPYRIGHT: Vitriol-nT, 2025, all rights reserved
import random

GRIDSIZE = 20

place = [[0 for _ in range(20)] for _ in range(20)]

def placefunction():
    n1 = random.randint(0, 19)
    n2 = random.randint(0, 19)
    return n1, n2

class Worm:
    def __init__(self, pointx = 2, pointy = 2):
        self.length = 5
        self.pointx = pointx
        self.pointy = pointy
        self.position = place[self.pointy][self.pointx]
        self.facing = "south"
        self.historyy = []
        self.historyx = []
        self.End = False
        #facing downwards at base.
    
    def death(self):
        self.End = True

    def moving(self, input):
        DirectionTrue = [False, False, False, False]
        #East, West, South, North
        #setting the facing side
        #cannot go through previous move selections
        if input == "u" and DirectionTrue[2] == False:
            self.facing = "north"
            if place[self.pointy - 1][self.pointx] == 1:
                self.death()
            else:
                self.pointy -= 1
            DirectionTrue = [False, False, False, True]
        elif input == "d" and DirectionTrue[3] == False:
            self.facing = "south"
            if place[self.pointy + 1][self.pointx] == 1:
                self.death()
            else:
                self.pointy += 1
            DirectionTrue = [False, False, True, False]
        elif input == "l" and DirectionTrue[0] == False:
            self.facing = "west"
            if place[self.pointy][self.pointx - 1] == 1:
                self.death()
            else:
                self.pointx -= 1
            DirectionTrue = [False, True, False, False]
        elif input == "r" and DirectionTrue[1] == False:
            self.facing = "east"
            if place[self.pointy][self.pointx + 1] == 1:
                self.death()
            else:
                self.pointx += 1
            DirectionTrue = [True, False, False, False]
        #at default, will be moving 1 pixel per .5 seconds for the heading direction

        if self.pointy < 0 or self.pointy > 19 or self.pointx < 0 or self.pointx > 19:
            self.death()

    def drawing(self):
        #The display will be on a web application. Only code for value change 0 to 1
        #move the head first, then rest will be tracing the parts
        self.historyx.append(self.pointx)
        self.historyy.append(self.pointy)
        
        for i in range(self.length):
            place[self.historyy[len(self.historyy) - 1 - i]][self.historyx[len(self.historyx) - 1 - i]] = 1
            place[self.historyy[len(self.historyy) - self.length - 1]][self.historyx[len(self.historyx) - self.length - 1]] = 0

class food:
    def __init__(self, pointxf, pointyf):
        self.pointxf = pointxf
        self.pointyf = pointyf
        self.score = 0

    def placement(self):
        n1, n2 = placefunction()
        if n1 is not None and n2 is not None and place[n2][n1] == 0:
            self.pointxf = n1
            self.pointyf = n2
            place[self.pointyf][self.pointxf] = 2
        else:
            self.placement()

    def eat(self, worm):
        if worm.pointx == self.pointxf and worm.pointy == self.pointyf:
            self.score += 1
            place[self.pointyf][self.pointxf] = 0
            self.placement()
            worm.length += 1

#Env setting
import numpy as np
class ActionSpace:
            def __init__(self):
                self.n = 4
            def sample(self):
                return random.randint(0, self.n - 1)

class WormEnv:
    def __init__(self):
        self.action_space = type('', (), {})()
        self.action_space.n = 4
        self.reset()  
        self.action_space = ActionSpace()
        self.reset()
        self.worm = Worm()
    
    def reset(self):
        global place
        place = [[0 for _ in range(GRIDSIZE)] for _ in range(GRIDSIZE)]
        self.worm = Worm(5, 5)
        self.food1 = food(10, 10)
        self.food1.placement()
        self.food2 = food(5, 6)
        self.food2.placement()
        self.steps = 0
        for _ in range(self.worm.length):
            self.worm.historyy.append(self.worm.pointy)
            self.worm.historyx.append(self.worm.pointx + 4 - _)
        state = self._get_state()
        return state, {}
    
    def step(self, action):
        self.worm.moving(action)
        self.food1.eat(self.worm)
        self.food2.eat(self.worm)
        self.worm.drawing()
        self.steps += 1

        reward = 0.1 if not self.worm.End else - 10
        if self.worm.pointx == self.food1.pointxf and self.worm.pointy == self.food1.pointyf:
            reward += 10
        if self.worm.pointx == self.food2.pointxf and self.worm.pointy == self.food2.pointyf:
            reward += 10
        
        done = self.worm.End or self.steps > 300

        state = self._get_state()
        return state, reward, done, False, {}

    def _get_state(self):
        return np.array(place, dtype=np.float32).flatten()
    
    def render(self):
        for row in place:
            print("".join(str(c) for c in row))
        print()