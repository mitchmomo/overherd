from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import ollama

import random
import os

app = Flask(__name__)
CORS(app)

location_to_topics = {
    "Stata Center": "6.033 (Computer Systems Engineering) is hard and has lots of papers and recitation participation; 6.004 (Computation Structures) has difficult exams and LAs are very helpful in office hours;  6.046 has killer psets and exams and the curve is insane", 
    "Simmons Hall": "the ball pit is gross but quirky; there are so many windows; the laundry sucks; stir fry is good in dining; concrete cave vibe", 
    "Lobby 7": "the columns are iconic; the dome is beautiful; so many tour groups; the rats are huge",
    "Killian Court": "ice skating on killian when it freezes; ultimate frisbee on the lawn; there are canadian geese everywhere; the view of the river is nice; nice place to nap",
    "Next House": "general culture is very nerdy, math/sci olympiad kids, but sweet people; Next Dining is the best, but sometimes there's way too much fish; the walk is so far; people need to shower and smell less bad; the mice are a problem; so many clubs and cool people; Next Sing is a great beginner friendly a capella group; there's a quant finance culture", 
    "East Campus": "murals are cool; floors have different cultures; more counterculture vibes; there's no dining hall; facilities are kinda really jank; big queer community; waking up 5 mins before class is nice",
    "Banana Lounge": "love free bananas; volunteers are cool; overhearing conversations in the lounge; people keep playing the piano while classes are happening and that's annoying",
    "Z Center": "asking about hot ppl they saw at the Z; big long lines for the machines",
    "Stud": "there are only 5 floors; people who talk in Stud 5 quiet side are annoying; Concord Market is overpriced; the new Stud 4 floor looks uncanny because it's so sterile; overhearing conversations is fun",
    "Infinite Corridor": "MITHenge (when the sunset lines up with the Infinite) is really cool; so busy between classes; people walk too slow; spotting people in the hallway; crush on cute ppl in the infinite (describe them)",
    "Green Building": "amazing view from the top; people do the green building stairs challenge and climb all the way up; there once was a tetris hack on the windows of the green building",
    "Kresge": "acapella group concerts; dance shows are fun; 2.009 final presentations are cool; people hang out on the lawn when the weather is nice",
    "Briggs Field": "the field is so big; the grass is always wet; frisbee is fun to play here; there are so many geese",
    "Hayden Library": "the chairs make you feel like you're falling over; people shouldn't talk on the second floor; eavesdropping on conversations is fun (here's what i overheard)",
}

with open("all_confessions_cleaned.json", "r") as f:
    all_confessions_cleaned = json.load(f)


def get_fewshot_examples():
    examples = random.sample(all_confessions_cleaned, 7)
    texts = [example["text"] for example in examples]
    return texts

def get_real_examples(location):
    with open("reference_confessions.json", "r") as f:
        reference_confessions = json.load(f)
    real_examples = reference_confessions.get(location, [])
    return real_examples

def generate_confession(location, examples):
    
    prompt = "Here are some anonymous MIT confessions:"
    for i, confession in enumerate(examples, 1):
        prompt += f"{i}. {confession}"
    
    prompt += "Write 42 new confessions about " + location + " in a similar voice, but make them significantly different from each other. Output as a json list. DO NOT use hashtags. DO NOT make your confessions poetic or I will kill you. Consider using the following as inspiration:" + location_to_topics[location]

    response = ollama.generate(model="mistral", prompt=prompt)
    return response["response"]
    

# Initialize a dictionary to store generated confessions for each location
generated_confessions = {}

# Load existing confessions from a file if it exists
confessions_file = "generated_confessions.json"
if os.path.exists(confessions_file):
    with open(confessions_file, "r") as f:
        generated_confessions = json.load(f)

@app.route("/confession", methods=["GET"])
def get_confession():
    location = request.args.get("location", "MIT")
    examples = get_fewshot_examples()
    confession = generate_confession(location, examples)
    
    # Add the generated confession to the dictionary
    if location not in generated_confessions:
        generated_confessions[location] = []
    generated_confessions[location].append(confession)
    
    # Save the updated confessions to the file
    with open(confessions_file, "w") as f:
        json.dump(generated_confessions, f, indent=4)
    
    return jsonify({"confession": confession, "sample_texts": examples})


@app.route("/gen_confession", methods=["GET"])
def gen_confession():
    location = request.args.get("location", "MIT")
    examples = get_real_examples(location)
    confession = generate_confession(location, examples)
    
    # Add the generated confession to the dictionary
    if location not in generated_confessions:
        generated_confessions[location] = []
    generated_confessions[location].append(confession)
    
    # Save the updated confessions to the file
    with open(confessions_file, "w") as f:
        json.dump(generated_confessions, f, indent=4)
    
    return jsonify({"confession": confession, "sample_texts": examples})

@app.route("/confession_db", methods=["GET"])
def get_confession_from_db():
    location = request.args.get("location", "MIT")
    if location in generated_confessions and generated_confessions[location]:
        confession = f"#{random.randint(243, 99999)}: {random.choice(generated_confessions[location])}"
        print(confession)
        return jsonify({"confession": confession})
    return get_confession()


@app.route("/guess_confession", methods=["GET"])
def guess_confession():
    location = request.args.get("location", None)
    
    with open("real_confessions.json", "r") as f:
        real_confessions = json.load(f)
    with open("fake_confessions.json", "r") as f:
        fake_confessions = json.load(f)

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
        "label": selected["label"]  # don't expose this to frontend unless verifying
    })



if __name__ == "__main__":
    app.run(debug=True)
