
from __future__ import annotations

import json
from typing import Any, List, Dict

from openai import OpenAI

from config import OPENAI_API_KEY, SYSTEM_PROMPT, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

def plan_actions(b64_image: str, user_command: str) -> List[Dict[str, Any]]:
    """Send screenshot + command to GPT-4o, get list of actions."""
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64_image}"
                    },
                },
                {
                    "type": "text",
                    "text": user_command,
                },
            ],
        },
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=300,
        temperature=0.1,
    )

    raw = response.choices[0].message.content.strip()

    try:
        data = json.loads(raw)
        return data.get("actions", [])
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Received non-JSON from model: {raw}") from e




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
                "Here is the current screen:",
                {
                    "mime_type": "image/png",
                    "data": b64_image,
                },
                "Based on above screen and task, plan actions in JSON.",
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



