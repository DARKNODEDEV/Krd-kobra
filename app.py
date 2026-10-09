import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

VENICE_API_KEY = os.environ.get("VENICE_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "نامە بەتاڵە"}), 400
    
    try:
        response = requests.post(
            "https://api.venice.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {VENICE_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "zai-org-glm-5-1",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. The user only understands Kurdish (Sorani) and English. Always respond in Kurdish or English. Never use Arabic, Persian, or Turkish."
                    },
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=60
        )
        data = response.json()
        return jsonify({"reply": data["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
