from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt kosong"}), 400

    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        return jsonify({"error": "Missing GEMINI_API_KEY"}), 500

    # Endpoint Gemini (harap cek dokumentasi resmi untuk endpoint yang benar)
    url = "https://generativeai.googleapis.com/v1beta2/models/gemini-pro:generateText"

    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "temperature": 0.7
        # Tambahkan parameter lain sesuai kebutuhan dan dokumentasi
    }

    try:
        r = requests.post(url, json=payload, headers=headers)
        if r.status_code == 200:
            res = r.json()
            # Contoh pengambilan output; sesuaikan dengan struktur response dari Gemini API
            output = res.get("candidates", [{}])[0].get("output", "")
            return jsonify({"response": output})
        else:
            return jsonify({"error": f"Error dari Gemini API: {r.text}"}), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
