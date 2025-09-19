from Module import *
import math
import random
import numpy as np
import time

ACTIONS = [0,1,2,3]
Q = {}

def get_state(worm, f1, f2):
    return (worm.pointx, worm.pointy, f1.pointxf, f1.pointyf, f2.pointxf, f2.pointyf)

def get_Q(state, action):
    return Q.get((state, action), 0.0)

def choose_action(state, epsilon=0.2):
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    qs = [get_Q(state,a) for a in ACTIONS]
    return int(np.argmax(qs))

def update_Q(state, action, reward, next_state, alpha=0.5, gamma=0.9):
    prev = get_Q(state, action)
    max_next = max([get_Q(next_state,a) for a in ACTIONS])
    Q[(state, action)] = prev + alpha * (reward + gamma * max_next - prev)

W1 = Worm(10, 9)
F1 = food(5, 4)
F2 = food(10, 10)
F1.score = 0
F2.score = 0
for _ in range(W1.length):
        W1.historyy.append(W1.pointy)
        W1.historyx.append(W1.pointx + 4 - _)

while True:  
    state = get_state(W1, F1, F2)
    action = choose_action(state, epsilon=0.3)
    table = {
        (0): ('u'),
        (1): ('d'),
        (2): ('l'),
        (3): ('r')
    }
    W1.moving(table[action])
    #Record = Record.append(action)

    reward = -0.01
    if W1.End:
        W1.End = False
        reward = -1
        print("ded")
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
        W1 = Worm(10, 9)
        F1 = food(5, 4)
        F2 = food(10, 10)
        W1.length = 5
        W1.historyx = []
        W1.historyy = []
        for _ in range(W1.length):
            W1.historyy.append(W1.pointy)
            W1.historyx.append(W1.pointx + 4 - _)
        continue

    elif F1.eat(W1) or F2.eat(W1):
        reward = 2.5
        next_state = get_state(W1, F1, F2)
    else:
        next_state = get_state(W1, F1, F2)

    update_Q(state, action, reward, next_state)

    W1.drawing()

    print("Worm:", (W1.pointx, W1.pointy), "Score:", F1.score + F2.score)
    print(f"({F1.pointxf},{F1.pointyf})")
    print(f"({F2.pointxf},{F2.pointyf})")
    print(action)
    
    time.sleep(0.1)
    
