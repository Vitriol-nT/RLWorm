#with time library exported when used in code, make the delay and forever loop to be on the course
import random

place = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

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
        #facing downwards at base.

    def moving(self, input):
        DirectionTrue = [False, False, False, False]
        global End
        End = False
        #East, West, South, North
        #setting the facing side
        #cannot go through previous move selections
        if input == "u" and DirectionTrue[2] == False:
            self.facing = "north"
            self.pointy -= 1
            DirectionTrue = [False, False, False, True]
        elif input == "d" and DirectionTrue[3] == False:
            self.facing = "south"
            self.pointy += 1
            DirectionTrue = [False, False, True, False]
        elif input == "l" and DirectionTrue[0] == False:
            self.facing = "west"
            self.pointx -= 1
            DirectionTrue = [False, True, False, False]
        elif input == "r" and DirectionTrue[1] == False:
            self.facing = "east"
            self.pointx += 1
            DirectionTrue = [True, False, False, False]
        else:
            End = True
        #at default, will be moving 1 pixel per .5 seconds for the heading direction

        if self.pointy < 0 or self.pointy > 19 or self.pointx < 0 or self.pointx > 19:
            End = True
        
        if self.position == 1:
            End = True
        else:
            pass

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

