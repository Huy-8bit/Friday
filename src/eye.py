"""Screen‑capture utilities (the agent's eyes)."""
from __future__ import annotations

import base64
import io
from typing import Tuple

import pyautogui
from PIL import Image


def capture_screen() -> tuple[str, Tuple[int, int]]:
    """Capture current screen and return (base64_png, (width, height))."""
    screenshot = pyautogui.screenshot()  # returns PIL Image
    width, height = screenshot.size
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    b64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return b64_data, (width, height)