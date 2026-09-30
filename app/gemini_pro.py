import os

import google.generativeai as genai

MODEL_NAME = "models/gemini-1.5-pro"


def generate_story(outline: list[dict], character_name: str, tone: str) -> list[dict]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)

    outline_text = "\n".join(
        f"Panel {p['panel_number']}: {p['title']}\n"
        f"Scene: {p['scene_description']}\n"
        f"Image prompt: {p['image_prompt']}"
        for p in outline
    )

    prompt = f"""
Expand the following 5-panel outline into a cohesive comic story.

Main character: {character_name}
Tone: {tone}

For every panel provide:
- caption: a short ambient/background caption
- narration: concise comic narration and/or character dialogue

Return ONLY valid JSON as an array of exactly 5 objects, each with:
panel_number, caption, narration

Do not add markdown fences or commentary.

Outline:
{outline_text}
"""
    response = model.generate_content(prompt)
    text = response.text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "", 1).replace("```", "").strip()

    import json
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("Gemini Pro did not return the expected JSON array.")
    data = json.loads(text[start:end + 1])

    if not isinstance(data, list) or len(data) != 5:
        raise ValueError("Expected story content for exactly 5 panels.")
    return data
