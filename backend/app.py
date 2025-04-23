from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import random
import os

app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Load real confessions
with open("real_confessions.json", "r") as f:
    real_confessions = json.load(f)

# Load fake confessions
with open("fake_confessions.json", "r") as f:
    fake_confessions = json.load(f)

@app.route("/guess_confession", methods=["GET"])
def guess_confession():
    location = request.args.get("location")
    choices = []

    if location:
        real = real_confessions.get(location, [])
        fake = fake_confessions.get(location, [])
        if real:
            choices.append({"text": random.choice(real), "label": "real"})
        if fake:
            choices.append({"text": random.choice(fake), "label": "fake"})
    else:
        for loc in real_confessions:
            for r in real_confessions[loc]:
                choices.append({"text": r, "label": "real"})
        for loc in fake_confessions:
            for f in fake_confessions[loc]:
                choices.append({"text": f, "label": "fake"})

    selected = random.choice(choices)
    return jsonify({
        "confession": selected["text"],
        "label": selected["label"]
    })

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(debug=True)