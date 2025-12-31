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
        nx, ny = self.pointx, self.pointy
        if input == "u":
            self.facing = "north"
            nx, ny = self.pointx, self.pointy - 1
        elif input == "d":
            self.facing = "south"
            nx, ny = self.pointx, self.pointy + 1
        elif input == "l":
            self.facing = "west"
            nx, ny = self.pointx - 1, self.pointy
        elif input == "r":
            self.facing = "east"
            nx, ny = self.pointx + 1, self.pointy

        if nx < 0 or nx >= GRIDSIZE or ny < 0 or ny >= GRIDSIZE:
            self.death()
            return
            
        if place[ny][nx] == 1:
            self.death()
            return
            
        self.pointx, self.pointy = nx, ny
    def drawing(self):
        self.historyx.append(self.pointx)
        self.historyy.append(self.pointy)

        hist_len = len(self.historyx)
        n_body = min(self.length, hist_len)
        for i in range(n_body):
            hx = self.historyx[hist_len - 1 - i]
            hy = self.historyy[hist_len - 1 - i]
            place[hy][hx] = 1

        place[self.pointy][self.pointx] = 3

        if hist_len > self.length:
            tail_i = hist_len - self.length - 1
            tx = self.historyx[tail_i]
            ty = self.historyy[tail_i]
            if 0 <= tx < GRIDSIZE and 0 <= ty < GRIDSIZE:
                place[ty][tx] = 0

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

reward = 0

class WormEnv:
    def __init__(self):
        self.action_space = type('', (), {})()
        self.action_space.n = 4
        self.reset()  
        self.action_space = ActionSpace()
        self.reset()
        self.worm = Worm()
    
    def _get_state(self):
        return np.array(place, dtype=np.float32).flatten()

    def reset(self):
        global place
        global reward
        place = [[0 for _ in range(GRIDSIZE)] for _ in range(GRIDSIZE)]
        self.worm = Worm(5, 5)
        self.food1 = food(10, 10)
        self.food1.placement()
        self.food2 = food(5, 7)
        self.food2.placement()
        self.steps = 0
        self.worm.length = 5
        for _ in range(self.worm.length):
            self.worm.historyy.append(self.worm.pointy)
            self.worm.historyx.append(self.worm.pointx + 4 - _)
        state = self._get_state()
        reward = 0
        return state, {}
    
    def step(self, action):
        global reward
        self.worm.moving(action)
        print(action)
        self.steps += 1
        print(f"pos({self.worm.pointx},{self.worm.pointy})")
        reward += 0.01
        if self.worm.pointx == self.food1.pointxf and self.worm.pointy == self.food1.pointyf:
            self.food1.eat(self.worm)
            reward += 50
            self.steps -= 10
        if self.worm.pointx == self.food2.pointxf and self.worm.pointy == self.food2.pointyf:
            self.food2.eat(self.worm)
            reward += 50
            self.steps -= 10
        
        self.worm.drawing()
        done = self.worm.End or self.steps > 200
        if done:
            reward -= 250
            print(f"Got score:{self.food1.score + self.food2.score}")
            print(f"with reward of: {reward}")
            print(place)
        state = self._get_state()
        return state, reward, done, False, {}
    
    def render(self):
        for row in place:
            print("".join(str(c) for c in row))
        print()
