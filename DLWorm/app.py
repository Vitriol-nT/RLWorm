from flask import Flask, render_template, request, jsonify
from Module import *
import numpy as np

app = Flask(__name__)

W1 = Worm(10, 9)
F1 = food(5, 4)
F2 = food(10, 10)
F1.placement()
F2.placement()
for _ in range(W1.length):
    W1.historyy.append(W1.pointy)
    W1.historyx.append(W1.pointx + 4 - _)

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/move', methods=['POST'])
def move():
    if W1.End:
        return '', 204

    data = request.get_json()
    direction = data.get('direction')

    if direction:
        W1.moving(direction)
        W1.drawing()
        F1.eat(W1)
        F2.eat(W1)

    return '', 204

@app.route('/state')
def get_state():
    score = F1.score + F2.score
    if W1.End:
        h = len(place)
        w = len(place[0]) if h > 0 else 0
        filled = [[2 for _ in range(w)] for _ in range(h)]
        return jsonify({'place': filled, 'score': score})
    else:
        pass

    return jsonify({'place': place, 'score': score})

@app.route('/finish')
def finish():
    End = W1.End
    return jsonify({'End': End})

import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

ACTION_MAP = {
    0: "u",
    1: "d",
    2: "l",
    3: "r",
}

class DQN(nn.Module):

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)

policy_net = DQN(400, 4)
policy_net.load_state_dict(torch.load("policy_weights.pth", map_location="cpu"))
policy_net.eval()

from A2Module import VirtualPlace, DQNworm, DQNfood

DW = DQNworm(5,5)
DF1 = DQNfood(4,4)
DF2 = DQNfood(6,6)
DF1.placement()
DF2.placement()

@app.route('/DQNmove', methods=['POST'])
def DQNmovement():
    if DW.End:
        return '', 204

    grid = np.array(VirtualPlace, dtype=np.float32)
    flat = grid.flatten()
    state_tensor = torch.tensor(flat, dtype=torch.float32).unsqueeze(0)

    with torch.no_grad():
        policy_net.eval()
        q_values = policy_net(state_tensor)
        action_idx = int(q_values.argmax(dim=1).item())

    DQNdirection = ACTION_MAP.get(action_idx)

    if DQNdirection is not None:
        DW.moving(DQNdirection)
        DF1.eat(DW)
        DF2.eat(DW)
        DW.drawing()
        print(VirtualPlace)
    return '', 204

@app.route('/DQNstate')
def get_stateDQN():
    score = DF1.score + DF2.score
    if DW.End:
        h = len(VirtualPlace)
        w = len(VirtualPlace[0]) if h > 0 else 0
        filled = [[2 for _ in range(w)] for _ in range(h)]
        return jsonify({'VirtualPlace': filled, 'score': score})
    else:
        pass
    return jsonify({'VirtualPlace': VirtualPlace, 'score': score})
@app.route('/DQNfinish')
def DQNfinish():
    End = DW.End
    return jsonify({'End': End})
if __name__ == '__main__':
    app.run(debug=True)
