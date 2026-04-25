import os
import json
import re
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT = """
Look at this fridge photo carefully.

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
}
"""


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
    image_part = {"mime_type": file.mimetype, "data": image_bytes}

    response = model.generate_content([PROMPT, image_part])
    text = response.text.strip()

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
