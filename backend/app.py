from flask import Flask, request, jsonify
import ollama  # or use OpenAI API
import random

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
