import json
import os
import re
from typing import Any

import google.generativeai as genai

MODEL_NAME = "models/gemini-1.5-flash"


def _extract_json(text: str) -> Any:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("Gemini Flash did not return a JSON array.")
    return json.loads(text[start:end + 1])


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> list[dict]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
Create a structured 5-panel comic outline for ComicCraft.

Story prompt: {story_prompt}
Main character name: {character_name}
Setting: {setting}
Story tone: {tone}
Art style: {art_style}

Return ONLY valid JSON as an array of exactly 5 objects.
Each object must contain:
- panel_number: integer 1-5
- title: short panel title
- scene_description: concise scene description
- image_prompt: detailed prompt for Stable Diffusion

Keep the character, setting, tone, and visual style consistent across all five panels.
Do not add markdown fences or extra commentary.
"""
    response = model.generate_content(prompt)
    data = _extract_json(response.text)

    if not isinstance(data, list) or len(data) != 5:
        raise ValueError("Expected exactly 5 comic panels.")
    return data
