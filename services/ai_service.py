
import os
import json
from google import genai
from google.genai import types


def analyze_food_image(image_bytes: bytes) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "mode": "error",
            "message": "Gemini API key is missing. Check Render Environment."
        }

    try:
        client = genai.Client(api_key=api_key)

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg"
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                "Identify the food in this image. Return only valid JSON with "
                "these fields: food_name, ingredients (list), "
                "nutrition (object containing calories, protein_g, "
                "carbs_g, fat_g per estimated serving), "
                "message. Give approximate nutrition values and clearly "
                "mention that they are estimates. If this is not food, "
                "identify that clearly.",
                image_part
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)

        return {
            "mode": "ai",
            "food_name": result.get("food_name", "Unknown food"),
            "ingredients": result.get("ingredients", []),
            "nutrition": result.get("nutrition"),
            "message": result.get(
                "message",
                "AI analysis completed. Nutrition values are estimates."
            )
        }

    except Exception as e:
        print("Gemini image analysis error:", str(e))
        return {
            "mode": "error",
            "message": "Food analysis failed. Please try another image."
        }


def chat_reply(message: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is not configured."

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="You are Food Verse AI, a helpful food and nutrition "
                     "assistant. Give safe, concise answers. Do not claim "
                     "medical certainty. User asks: " + message
        )

        return response.text or "Please try asking again."

    except Exception as e:
        print("Gemini chat error:", str(e))
        return "Sorry, the AI assistant is temporarily unavailable."
