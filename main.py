from flask import Flask, request, jsonify
import json
import difflib

app = Flask(__name__)

data_file = "datasets/furbotv2_2.jsonl"


def load_data():
    conversations = []
    with open(data_file, "r", encoding="utf-8") as file:
        for line in file:
            conversations.append(json.loads(line))
    return conversations


def find_best_match(user_input, dataset):
    user_messages = [conv["messages"][-2]["content"] for conv in dataset if len(conv["messages"]) >= 2]
    closest_matches = difflib.get_close_matches(user_input, user_messages, n=1, cutoff=0.7)

    if closest_matches:
        for conv in dataset:
            if len(conv["messages"]) >= 2 and conv["messages"][-2]["content"] == closest_matches[0]:
                return conv["messages"][-1]["content"]
    return "I'm sorry, I don't have an answer for that. Please contact the Mandaue City Veterinary Office for more information."


@app.route("/chat", methods=["POST"])
def chat():
    user_data = request.get_json()
    user_message = user_data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    dataset = load_data()
    response = find_best_match(user_message, dataset)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
