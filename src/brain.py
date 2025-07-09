from __future__ import annotations

import os
import json
import re
from typing import Any, List, Dict

import google.generativeai as genai
from config import SYSTEM_PROMPT

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("⚠️ Please set GEMINI_API_KEY in .env")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"

def plan_actions(session_history: List[Dict[str, str]], b64_image: str) -> List[Dict[str, Any]]:
    """
    Sends full conversation + current screen to Gemini,
    receives plan (JSON list of actions)
    """
    content = [
        {"role": "user", "parts": SYSTEM_PROMPT},
        *session_history,
        {
            "role": "user",
            "parts": [
                "Here is the current screen (resolution: 1920x1080) with grid lines every 100 pixels:",
                {
                    "mime_type": "image/png",
                    "data": b64_image,
                },
                "Use the grid lines to estimate pixel coordinates more accurately. Plan GUI actions in JSON using absolute coordinates relative to 1920x1080."
            ]
        }
    ]

    response = model.generate_content(
        contents=content,
        generation_config={
            "temperature": 0.3,
            "max_output_tokens": 1024,
        },
    )

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*\n", "", raw)
        raw = re.sub(r"\n?```$", "", raw)

    raw = raw.strip()

    try:
        parsed = json.loads(raw)
        return parsed.get("actions", [])
    except json.JSONDecodeError as e:
        print("[DEBUG] Gemini raw output:\n", repr(raw))
        raise RuntimeError("Gemini returned invalid JSON.") from e
