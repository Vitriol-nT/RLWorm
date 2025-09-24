#I needed to make another file
#previous code was built with absolute no mind
#Basically copy of Module.py tailored for Agent
import random


VirtualPlace = [[0 for _ in range(20)] for _ in range(20)]

def placefunction():
    n1 = random.randint(0, 19)
    n2 = random.randint(0, 19)
    return n1, n2

class DQNworm:
    def __init__(self, pointx = 2, pointy = 2):
        self.length = 5
        self.pointx = pointx
        self.pointy = pointy
        self.position = VirtualPlace[self.pointy][self.pointx]
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
            if VirtualPlace[self.pointy - 1][self.pointx] == 1:
                self.death()
            else:
                self.pointy -= 1
            DirectionTrue = [False, False, False, True]
        elif input == "d" and DirectionTrue[3] == False:
            self.facing = "south"
            if VirtualPlace[self.pointy + 1][self.pointx] == 1:
                self.death()
            else:
                self.pointy += 1
            DirectionTrue = [False, False, True, False]
        elif input == "l" and DirectionTrue[0] == False:
            self.facing = "west"
            if VirtualPlace[self.pointy][self.pointx - 1] == 1:
                self.death()
            else:
                self.pointx -= 1
            DirectionTrue = [False, True, False, False]
        elif input == "r" and DirectionTrue[1] == False:
            self.facing = "east"
            if VirtualPlace[self.pointy][self.pointx + 1] == 1:
                self.death()
            else:
                self.pointx += 1
            DirectionTrue = [True, False, False, False]
        #at default, will be moving 1 pixel per .5 seconds for the heading direction

        if self.pointy < 0 or self.pointy > 19 or self.pointx < 0 or self.pointx > 19:
            self.death()

    def get_state(self):
        return np.array(VirtualPlace, dtype=np.float32).flatten()

    def drawing(self):
        #The display will be on a web application. Only code for value change 0 to 1
        #move the head first, then rest will be tracing the parts
        self.historyx.append(self.pointx)
        self.historyy.append(self.pointy)
        
        for i in range(self.length):
            VirtualPlace[self.historyy[len(self.historyy) - 1 - i]][self.historyx[len(self.historyx) - 1 - i]] = 1
            VirtualPlace[self.historyy[len(self.historyy) - self.length - 1]][self.historyx[len(self.historyx) - self.length - 1]] = 0

class DQNfood:
    def __init__(self, pointxf, pointyf):
        self.pointxf = pointxf
        self.pointyf = pointyf
        self.score = 0

    def placement(self):
        n1, n2 = placefunction()
        if n1 is not None and n2 is not None and VirtualPlace[n2][n1] == 0:
            self.pointxf = n1
            self.pointyf = n2
            VirtualPlace[self.pointyf][self.pointxf] = 2
        else:
            self.placement()

    def eat(self, worm):
        if worm.pointx == self.pointxf and worm.pointy == self.pointyf:
            self.score += 1
            VirtualPlace[self.pointyf][self.pointxf] = 0
            self.placement()
            worm.length += 1
