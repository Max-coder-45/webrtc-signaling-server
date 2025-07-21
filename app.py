# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

rooms = {}

@app.route('/offer', methods=['POST'])
def offer():
    data = request.json
    room_id = data['room']
    rooms[room_id] = {'offer': data['offer'], 'answer': None, 'candidates': []}
    return jsonify({'status': 'offer stored'})

@app.route('/get-offer/<room_id>', methods=['GET'])
def get_offer(room_id):
    room = rooms.get(room_id)
    return jsonify({'offer': room['offer']}) if room else ('', 404)

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    room_id = data['room']
    if room_id in rooms:
        rooms[room_id]['answer'] = data['answer']
        return jsonify({'status': 'answer stored'})
    return ('', 404)

@app.route('/get-answer/<room_id>', methods=['GET'])
def get_answer(room_id):
    room = rooms.get(room_id)
    return jsonify({'answer': room['answer']}) if room and room['answer'] else ('', 404)

@app.route('/candidate', methods=['POST'])
def candidate():
    data = request.json
    room_id = data['room']
    candidate = data['candidate']
    if room_id in rooms:
        rooms[room_id]['candidates'].append(candidate)
        return jsonify({'status': 'candidate stored'})
    return ('', 404)

@app.route('/get-candidates/<room_id>', methods=['GET'])
def get_candidates(room_id):
    room = rooms.get(room_id)
    return jsonify({'candidates': room['candidates']}) if room else ('', 404)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
