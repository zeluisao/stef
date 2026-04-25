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
MODELS_URL = "https://openrouter.ai/api/v1/models"

RECIPE_PROMPT = """You are a helpful cooking assistant.

I have these ingredients available: {ingredients}

Using ONLY these ingredients, suggest one {meal} recipe with clear step-by-step cooking instructions.

Respond with ONLY valid JSON in exactly this format (no markdown, no extra text):
{{
  "name": "Recipe Name",
  "ingredients_used": ["item1", "item2"],
  "steps": ["Step 1: ...", "Step 2: ..."]
}}"""


def fetch_models():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resp = requests.get(MODELS_URL, headers=headers, timeout=10)
    return resp.json().get("data", [])


def find_vision_model(models):
    for m in models:
        mid = m.get("id", "")
        if not mid.endswith(":free"):
            continue
        arch = m.get("architecture", {})
        modalities = arch.get("input_modalities", arch.get("modalities", []))
        if "image" in modalities:
            print("Vision model:", mid)
            return mid
    return None


def find_text_model(models):
    skip = ["ocr", "embed", "whisper", "tts", "rerank", "vision"]
    for m in models:
        mid = m.get("id", "")
        if not mid.endswith(":free"):
            continue
        if any(kw in mid.lower() for kw in skip):
            continue
        arch = m.get("architecture", {})
        modalities = arch.get("output_modalities", arch.get("modalities", []))
        if "text" in modalities or not modalities:
            print("Text model:", mid)
            return mid
    return None


try:
    all_models = fetch_models()
    VISION_MODEL = find_vision_model(all_models)
    TEXT_MODEL = find_text_model(all_models)
    print(f"Vision: {VISION_MODEL} | Text: {TEXT_MODEL}")
except Exception as e:
    print("Could not fetch models:", e)
    VISION_MODEL = None
    TEXT_MODEL = None


def call_model(model, messages):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages}
    resp = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)
    print("Status:", resp.status_code, "| Response:", resp.text[:300])
    return resp.json()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    files = request.files.getlist("image")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "No image uploaded"}), 400

    meal = request.form.get("meal", "breakfast")

    if not VISION_MODEL or not TEXT_MODEL:
        return jsonify({"error": "Could not find available free models"}), 500

    # Build image parts for all uploaded photos
    image_parts = []
    for file in files[:5]:
        image_bytes = file.read()
        image_b64 = base64.b64encode(image_bytes).decode()
        data_url = f"data:{file.mimetype};base64,{image_b64}"
        image_parts.append({"type": "image_url", "image_url": {"url": data_url}})

    # Step 1: use vision model to identify ingredients across all images
    vision_content = [{"type": "text", "text": "List every food item and ingredient you can see in these fridge photos. Return only a plain comma-separated list of ingredients, nothing else."}]
    vision_content.extend(image_parts)

    vision_data = call_model(VISION_MODEL, [
        {"role": "user", "content": vision_content}
    ])

    if "choices" not in vision_data:
        return jsonify({"error": f"Vision model error: {vision_data}"}), 500

    ingredients_text = vision_data["choices"][0]["message"]["content"].strip()
    print("Ingredients found:", ingredients_text)

    # Step 2: use text model to generate recipe for chosen meal
    recipe_data = call_model(TEXT_MODEL, [
        {
            "role": "user",
            "content": RECIPE_PROMPT.format(ingredients=ingredients_text, meal=meal)
        }
    ])

    if "choices" not in recipe_data:
        return jsonify({"error": f"Recipe model error: {recipe_data}"}), 500

    text = recipe_data["choices"][0]["message"]["content"].strip()

    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if not json_match:
        return jsonify({"error": "Could not parse recipe response"}), 500

    try:
        recipe = json.loads(json_match.group())
        result = {
            "ingredients": [i.strip() for i in ingredients_text.split(",") if i.strip()],
            "recipe": recipe
        }
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON from recipe model"}), 500

    return jsonify(result)


CHAT_SYSTEM = """You are a friendly cooking assistant. The user has these ingredients in their fridge: {ingredients}.
They are looking for a {meal} recipe. Help them adjust or replace the recipe based on their requests.
If you suggest a new or modified recipe, include it as JSON inside a <recipe> tag like this:
<recipe>{{"name": "...", "ingredients_used": [...], "steps": [...]}}</recipe>
Otherwise just reply conversationally."""


@app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json()
    message     = body.get("message", "")
    ingredients = body.get("ingredients", [])
    meal        = body.get("meal", "breakfast")
    history     = body.get("history", [])

    if not TEXT_MODEL:
        return jsonify({"error": "No text model available"}), 500

    system_msg = CHAT_SYSTEM.format(ingredients=", ".join(ingredients), meal=meal)
    messages   = [{"role": "system", "content": system_msg}] + history

    data = call_model(TEXT_MODEL, messages)

    if "choices" not in data:
        return jsonify({"error": str(data)}), 500

    reply_text = data["choices"][0]["message"]["content"].strip()

    recipe = None
    recipe_match = re.search(r"<recipe>(.*?)</recipe>", reply_text, re.DOTALL)
    if recipe_match:
        try:
            recipe = json.loads(recipe_match.group(1).strip())
        except json.JSONDecodeError:
            pass
        reply_text = re.sub(r"<recipe>.*?</recipe>", "", reply_text, flags=re.DOTALL).strip()

    return jsonify({"reply": reply_text, "recipe": recipe})


if __name__ == "__main__":
    app.run(debug=True)
