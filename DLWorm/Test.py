from Module import *
from PIL import Image
import numpy as np


W1 = Worm(3, 3)
F1 = food(5,4)
F1.placement()
F2 = food(10, 10)
F2.placement()

#This thing is needed to start because at start, the history list does not have
#previous track of the head moving. So just for enough the length to start, same startpoint is used
for _ in range(W1.length):
    W1.historyy.append(W1.pointy)
    W1.historyx.append(W1.pointx)

#Moving, Drawing, and Eat are the 1 sets each move

for i in range(10):
    W1.moving("d")
    W1.drawing()
    F1.eat(W1)
    F2.eat(W1)
    W1.moving("r")
    W1.drawing()
    F1.eat(W1)
    F2.eat(W1)
    array = np.array(place, dtype=np.uint8) * 255
    img = Image.fromarray(array, mode='L')
    img.save(f"Stat_{i}.png")
    print(F1.score + F2.score)

for i in range(5):
    W1.moving("u")
    W1.drawing()
    F1.eat(W1)
    F2.eat(W1)
    array = np.array(place, dtype=np.uint8) * 255
    img = Image.fromarray(array, mode='L')
    img.save(f"Stat_{i+10}.png")
    print(F1.score + F2.score)

#Now its working as it should've been.
