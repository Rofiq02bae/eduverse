from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt kosong"}), 400

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        res = requests.post(url, headers=headers, params=params, json=body)
        res_json = res.json()
        if "candidates" in res_json:
            reply = res_json["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"response": reply})
        else:
            return jsonify({"error": res_json}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500