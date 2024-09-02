from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

STATUS_FILE = 'service_scores.json'

@app.route('/')
def scoreboard():
    return render_template('scoreboard.html')

@app.route('/status')
def status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)