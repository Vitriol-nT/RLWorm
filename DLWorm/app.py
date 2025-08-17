from flask import Flask, render_template, request, jsonify
from Module import *

app = Flask(__name__)

W1 = Worm(3, 3)
F1 = food(5, 4)
F2 = food(10, 10)
F1.placement()
F2.placement()
for _ in range(W1.length):
    W1.historyy.append(W1.pointy)
    W1.historyx.append(W1.pointx)

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/move', methods=['POST'])
def move():
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
    return jsonify({'place': place, 'score': score})

if __name__ == '__main__':
    app.run(debug=True)
