from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# File to store high scores
SCORES_FILE = 'high_scores.json'

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scores', methods=['GET'])
def get_scores():
    scores = load_scores()
    top_scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:10]
    return jsonify(top_scores)

@app.route('/api/scores', methods=['POST'])
def add_score():
    data = request.get_json()
    if not data or 'name' not in data or 'score' not in data:
        return jsonify({'error': 'Name and score are required'}), 400
    
    scores = load_scores()
    scores.append({
        'name': data['name'],
        'score': data['score']
    })
    save_scores(scores)
    
    return jsonify({'message': 'Score added successfully'}), 201

if __name__ == '__main__':
    # Create high_scores.json if it doesn't exist
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w') as f:
            json.dump([], f)
    
    app.run(debug=True)