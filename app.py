import os
import json
import re
import base64
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

with open("api_key.txt", encoding="utf-8-sig") as f:
    API_KEY = f.read().strip()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "qwen/qwen2.5-vl-72b-instruct:free"

PROMPT = """Look at this fridge photo carefully.

1. List every food item and ingredient you can see.
2. Using ONLY those ingredients, suggest one recipe each for breakfast, lunch, and dinner with clear step-by-step cooking instructions.

Respond with ONLY valid JSON in exactly this format (no markdown, no extra text):
{
  "ingredients": ["item1", "item2"],
  "breakfast": {
    "name": "Recipe Name",
    "ingredients_used": ["item1", "item2"],
    "steps": ["Step 1: ...", "Step 2: ..."]
  },
  "lunch": {
    "name": "Recipe Name",
    "ingredients_used": ["item1", "item2"],
    "steps": ["Step 1: ...", "Step 2: ..."]
  },
  "dinner": {
    "name": "Recipe Name",
    "ingredients_used": ["item1", "item2"],
    "steps": ["Step 1: ...", "Step 2: ..."]
  }
}"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    image_bytes = file.read()
    image_b64 = base64.b64encode(image_bytes).decode()
    data_url = f"data:{file.mimetype};base64,{image_b64}"

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)
        print("Status:", resp.status_code)
        print("Response:", resp.text[:500])
        data = resp.json()
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

    if "choices" not in data:
        return jsonify({"error": str(data)}), 500

    text = data["choices"][0]["message"]["content"].strip()

    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if not json_match:
        return jsonify({"error": "Could not parse AI response"}), 500

    try:
        result = json.loads(json_match.group())
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON from AI"}), 500

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
