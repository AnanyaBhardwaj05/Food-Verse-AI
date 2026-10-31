from flask import Flask, request, jsonify
from flask_cors import CORS
from services.ai_service import analyze_food_image, chat_reply
from services.food_data import NUTRITION, RECIPES
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
ALLOWED = {"png", "jpg", "jpeg", "webp"}

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "app": "Food Verse AI", "mode": "demo"})

@app.post("/api/analyze")
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "Please upload a food image."}), 400
    image = request.files["image"]
    ext = image.filename.rsplit(".", 1)[-1].lower() if "." in image.filename else ""
    if ext not in ALLOWED:
        return jsonify({"error": "Supported formats: JPG, JPEG, PNG, WEBP."}), 400
    try:
        raw = image.read()
        Image.open(BytesIO(raw)).verify()
    except Exception:
        return jsonify({"error": "The uploaded file is not a valid image."}), 400
    result = analyze_food_image(raw)
    return jsonify(result)

@app.get("/api/nutrition")
def nutrition():
    food = request.args.get("food", "").strip().lower()
    if not food:
        return jsonify({"error": "Enter a food name."}), 400
    match = NUTRITION.get(food)
    if not match:
        return jsonify({"food": food.title(), "available": False,
                        "message": "No demo nutrition entry found. Connect a nutrition data provider for broader coverage."})
    return jsonify({"food": food.title(), "available": True, "per_serving": match,
                    "note": "Approximate demo values; portion size and preparation change nutrition."})

@app.post("/api/recipes")
def recipes():
    data = request.get_json(silent=True) or {}
    ingredients = [x.strip().lower() for x in data.get("ingredients", []) if isinstance(x, str) and x.strip()]
    matches = []
    for recipe in RECIPES:
        overlap = [x for x in recipe["ingredients"] if x in ingredients]
        if overlap:
            matches.append({**recipe, "matched_ingredients": overlap})
    return jsonify({"recipes": matches[:6]})

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Type a message first."}), 400
    return jsonify({"reply": chat_reply(message), "mode": "demo"})

@app.errorhandler(413)
def too_large(_):
    return jsonify({"error": "Image is too large. Maximum size is 8 MB."}), 413

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
