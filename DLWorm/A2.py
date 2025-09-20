import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
import time
from collections import deque
from Module import *
    
ACTIONS = [0, 1, 2, 3]
STATE_SIZE = 6
ACTION_SIZE = len(ACTIONS)
GAMMA = 0.9
LR = 1e-3
BATCH_SIZE = 64
MEMORY_SIZE = 5000
EPSILON_START = 1.0
EPSILON_MIN = 0.05
EPSILON_DECAY = 0.995
TARGET_UPDATE = 50

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define Q-Network
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_size)
        )

    def forward(self, x):
        return self.fc(x)

# Initialize networks
policy_net = DQN(STATE_SIZE, ACTION_SIZE).to(device)
target_net = DQN(STATE_SIZE, ACTION_SIZE).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=LR)
memory = deque(maxlen=MEMORY_SIZE)

epsilon = EPSILON_START
steps_done = 0

def get_state(worm, f1, f2):
    return np.array([worm.pointx, worm.pointy, f1.pointxf, f1.pointyf, f2.pointxf, f2.pointyf], dtype=np.float32)

def choose_action(state):
    global epsilon, steps_done
    steps_done += 1
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    with torch.no_grad():
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        q_values = policy_net(state)
        return int(torch.argmax(q_values).item())

def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    
    batch = random.sample(memory, BATCH_SIZE)
    states, actions, rewards, next_states, dones = zip(*batch)
    states = torch.tensor(np.array(states), dtype=torch.float32, device=device)
    actions = torch.tensor(actions, dtype=torch.long, device=device).unsqueeze(1)
    rewards = torch.tensor(np.array(rewards), dtype=torch.float32, device=device).unsqueeze(1)
    next_states = torch.tensor(np.array(next_states), dtype=torch.float32, device=device)
    dones = torch.tensor(np.array(dones, dtype=np.float32), device=device).unsqueeze(1)

    # Q(s,a)
    q_values = policy_net(states).gather(1, actions)

    # Q_target(s',a')
    with torch.no_grad():
        max_next_q = target_net(next_states).max(1)[0].unsqueeze(1)
        target = rewards + (1 - dones) * GAMMA * max_next_q

    # Loss
    loss = nn.MSELoss()(q_values, target)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Reset game function
def reset_game():
    global place
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

def set_env():
    global W1
    global F1
    global F2
    W1 = Worm(10, 9)
    W1.historyx = []
    W1.historyy = []
    for _ in range(W1.length):
        W1.historyy.append(W1.pointy)
        W1.historyx.append(W1.pointx + 4 - _)
    F1 = food(5, 4)
    F2 = food(10, 10)
    F1.placement()
    F2.placement()

set_env() #initial Environment

target_update_counter = 0
deathcounter = 0
while True:
    done = False
    state = get_state(W1, F1, F2)
    action = choose_action(state)
    table = {0: 'u', 1: 'd', 2: 'l', 3: 'r'}
    W1.moving(table[action])
    W1.drawing()
    F1.eat(W1)
    F2.eat(W1)
    reward = -0.01

    if W1.End:
        reward = -1
        done = True
        print("Worm died!")
        deathcounter += 1
        if deathcounter > 20:
            print("bug.")
            break
    elif F1.eat(W1) or F2.eat(W1):
        reward = 10
    else:
        pass
    next_state = get_state(W1, F1, F2)
    memory.append((state, action, reward, next_state, done))
    optimize_model()

    # Update target network
    if target_update_counter % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
    target_update_counter += 1

    if epsilon > EPSILON_MIN:
        epsilon *= EPSILON_DECAY

    if done:
        reset_game()
        set_env()
        continue

    print(place)
    print("Score:", F1.score + F2.score, "Last action:", action)

    time.sleep(0.25)
