import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = "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"

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.json["prompt"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"response": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)