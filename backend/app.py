# from flask import Flask, request, jsonify
# import ollama  # or use OpenAI API
# import random

# app = Flask(__name__)

from flask import Flask, jsonify, request
from flask_cors import CORS

import random

app = Flask(__name__)
CORS(app)

# Placeholder confessions (will replace with LLM later)
confessions = {
    "stata": [
        "I once stayed in Stata for 48 hours straight, surviving only on Soylent and coffee.",
        "Sometimes I pretend to be on a call just to avoid talking to recruiters here.",
        "The Stata bathrooms are my secret napping spot. Don't tell anyone."
    ],
    "simmons": [
        "I got lost in Simmons my first week and had to ask for directions to my own dorm room.",
        "I don't actually live in Simmons, I just say I do for the clout.",
        "The architecture is cool, but why does it feel like a dystopian cheese grater?"
    ],
    "killian": [
        "I graduated last year and still have nightmares about running naked through Killian.",
        "One time I saw a goose chase a freshman across Killian. It was majestic.",
        "Every time I sit here, I wonder if I’ll actually graduate or just vibe forever."
    ],
    "lobby7": [
        "I used to believe that the Infinite Corridor actually never ended.",
        "One time, I got trapped in a tourist group and just went along with it.",
        "Lobby 7 smells different every time I walk in, and I don't know why."
    ]
}

@app.route('/confession', methods=['GET'])
def get_confession():
    location = request.args.get("location", "MIT")
    if location in confessions:
        confession = random.choice(confessions[location])
        return jsonify({"confession": confession})
    return jsonify({"confession": "No confessions found for this location."})

if __name__ == '__main__':
    app.run(debug=True)


# def get_fewshot_examples(location):
#     topic_id = location_to_topic.get(location, None)
#     if topic_id is not None:
#         topic_confessions = [
#             text for text, topic in confessions.items() if topic == topic_id
#         ]
#         return random.sample(topic_confessions, min(5, len(topic_confessions)))  # Pick 5 or fewer
#     return ["No confessions found for this location."]

# def generate_confession(location):
#     prompt = f"Write an anonymous MIT confession about {location} in the style of MIT Confessions."
#     response = ollama.generate(model="mistral", prompt=prompt)
#     return response["response"]  # Adjust based on LLM output format

# @app.route("/confession", methods=["GET"])
# def get_confession():
#     location = request.args.get("location", "MIT")
#     confession = generate_confession(location)
#     return jsonify({"confession": confession})

# if __name__ == "__main__":
    # app.run(debug=True)
