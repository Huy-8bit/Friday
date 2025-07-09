from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("⚠️  Please set OPENAI_API_KEY env var or .env file before running agent.")

MODEL_NAME: str = "gpt-4o"
IMAGE_TOKEN_BUDGET: int = 6_000

SYSTEM_PROMPT: str = (
    "You are an intelligent desktop assistant. Given a task and a screenshot, "
    "you must plan step-by-step what GUI actions to perform to help the user.\n\n"

    "Only reply with JSON following this schema:\n"
    "{ \"actions\": [ { \"type\": ..., ... } ] }\n\n"

    "Valid actions include:\n"
    "- open_app: { \"type\": \"open_app\", \"app\": \"Slack\" }\n"
    "- click: { \"type\": \"click\", \"x\": 100, \"y\": 200 }\n"
    "- type: { \"type\": \"type\", \"text\": \"hello huy\" }\n"
    "- key: { \"type\": \"key\", \"keys\": \"enter\" }\n"
    "- wait: { \"type\": \"wait\", \"seconds\": 1.5 }\n\n"

    "Instructions:\n"
    "- Always click input fields or buttons before typing.\n"
    "- Use 'wait' after opening web pages or switching apps.\n"
    "- Avoid repeating actions that didn’t result in changes.\n"
    "- Use coordinates relative to a 1920x1080 screen with 100px grid lines.\n"
    "- You may assume the user interface is rendered in English.\n\n"

    "Examples:\n"
    "1. To search on YouTube: click the search bar, type query, press enter.\n"
    "2. To open Notepad and type: open app, wait, type text.\n\n"

    "If no actions are needed, return: { \"actions\": [] }"
)

GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT: str = os.getenv("GEMINI_ENDPOINT", "https://api.gemini.com/v1")

if not GEMINI_API_KEY:
    raise RuntimeError("⚠️  Please set GEMINI_API_KEY env var or .env file before running agent.")