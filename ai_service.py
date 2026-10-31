def analyze_food_image(image_bytes: bytes) -> dict:
    # Safe demo behavior: no real image recognition is claimed here.
    # Add a vision-model provider call here when API credentials are configured.
    return {
        "mode": "demo",
        "food_name": "Food image received",
        "ingredients": ["Image uploaded successfully"],
        "nutrition": None,
        "message": "Demo mode: the image upload works, but a vision AI provider is not configured. Connect a model in this service for real food recognition."
    }

def chat_reply(message: str) -> str:
    q = message.lower()
    if "calorie" in q or "nutrition" in q:
        return "I can share approximate nutrition for foods in the demo database. Try asking about idli, dosa, dal, paneer, biryani, apple, or banana."
    if "recipe" in q or "cook" in q:
        return "Tell me the ingredients you have, separated by commas, and use the Recipe Finder to see matching ideas."
    if "healthy" in q:
        return "A balanced plate often includes vegetables or fruit, a protein source, whole grains, and water. Your needs may vary."
    return "I'm Food Verse AI in demo mode. I can help explore food, nutrition estimates, and recipe ideas. For live AI answers, configure a provider in the backend."
