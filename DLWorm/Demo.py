from Module import *

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

while True:
  a = input("Enter direction (u/d/l/r): ")
  b = (F1.score + F2.score)
  if a in ["u", "d", "l", "r"]:
      W1.moving(a)
      W1.drawing()
      F1.eat(W1)
      F2.eat(W1)
      print(place)
      print(b)

#Now works perfectly.