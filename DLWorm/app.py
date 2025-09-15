from flask import Flask, render_template, request, jsonify
from Module import *

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


if __name__ == '__main__':
    app.run(debug=True)
