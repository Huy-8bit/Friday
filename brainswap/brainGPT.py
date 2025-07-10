# =========================
# File: brain.py (OpenAI version)
# -------------------------
from __future__ import annotations

import os
import json
import re
import base64
from typing import Any, List, Dict

from openai import OpenAI
from config import SYSTEM_PROMPT, OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

def plan_actions(session_history: List[Dict[str, str]], b64_image: str) -> List[Dict[str, Any]]:
    """
    Sends full conversation + current screen to OpenAI GPT model (e.g. gpt-4o),
    receives plan (JSON list of actions)
    """
    image_data = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/png;base64,{b64_image}"
        }
    }

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *[
            {"role": item["role"], "content": str(item["parts"])}
            for item in session_history
        ],
        {
            "role": "user",
            "content": [
                "Here is the current screen:",
                image_data,
                "Based on above screen and task, plan actions in JSON."
            ]
        }
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.3,
        max_tokens=1024,
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*\n", "", raw)
        raw = re.sub(r"\n?```$", "", raw)

    raw = raw.strip()

    try:
        parsed = json.loads(raw)
        return parsed.get("actions", [])
    except json.JSONDecodeError as e:
        print("[DEBUG] OpenAI raw output:\n", repr(raw))
        raise RuntimeError("OpenAI returned invalid JSON.") from e