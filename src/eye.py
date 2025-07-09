from __future__ import annotations

import base64
import io
from typing import Tuple

import pyautogui
from PIL import Image, ImageDraw

def draw_grid(image: Image.Image, spacing: int = 100) -> Image.Image:
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for x in range(0, width, spacing):
        draw.line((x, 0, x, height), fill=(200, 200, 200), width=1)
    for y in range(0, height, spacing):
        draw.line((0, y, width, y), fill=(200, 200, 200), width=1)
    return image

def capture_screen() -> tuple[str, Tuple[int, int]]:
    """Capture current screen and return (base64_png, (width, height))."""
    screenshot = pyautogui.screenshot()  # returns PIL Image
    screenshot = draw_grid(screenshot, spacing=100)
    width, height = screenshot.size
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    b64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return b64_data, (width, height)
