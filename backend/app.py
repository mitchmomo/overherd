from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import ollama

import random

app = Flask(__name__)
CORS(app)

location_to_topics = {
    "Stata Center": ["6.033 (Computer Systems Engineering) is hard and has lots of papers and recitation participation", "6.004 (Computation Structures) has difficult exams and LAs are very helpful in office hours", "6.046 has killer psets and exams and the curve is insane", "Comment on the food", "Comment on the study spaces", "Comment on the people"],
    "Simmons Hall": ["the ball pit is gross but quirky", "there are so many windows", "the laundry sucks", "stir fry is good in dining"],
    "Lobby 7": ["the columns are iconic", "the dome is beautiful", "the floor is slippery", "the chairs are uncomfortable"],
    "Killian Court": ["ice skating on killian when it freezes", "ultimate frisbee on the lawn", "there are canadian geese everywhere", "the view of the river is nice"],
}

with open("all_confessions_cleaned.json", "r") as f:
    all_confessions_cleaned = json.load(f)


def get_fewshot_examples():
    examples = random.sample(all_confessions_cleaned, 7)
    texts = [example["text"] for example in examples]
    return texts

def generate_confession(location, examples):
    
    prompt = "Here are five anonymous MIT confessions:\n\n"
    for i, confession in enumerate(examples, 1):
        prompt += f"{i}. {confession}\n"
    
    prompt += "\nWrite a single new confession about " + location + " in a similar voice. DO NOT use hashtags. Consider using the following as inspiration:\n" + random.choice(location_to_topics[location])

    response = ollama.generate(model="mistral", prompt=prompt)
    return response["response"]

@app.route("/confession", methods=["GET"])
def get_confession():
    location = request.args.get("location", "MIT")
    examples = get_fewshot_examples()
    confession = generate_confession(location, examples)
    return jsonify({"confession": confession, "sample_texts": examples})
 

if __name__ == "__main__":
    app.run(debug=True)
