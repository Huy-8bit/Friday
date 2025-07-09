"""Action executors (the agent's hands)."""
from __future__ import annotations

import time
from typing import Any, Dict, List

import keyboard
import pyautogui


def _perform_click(action: Dict[str, Any]):
    x = int(action["x"])
    y = int(action["y"])
    pyautogui.moveTo(x, y, duration=0.15)
    pyautogui.click()


def _perform_type(action: Dict[str, Any]):
    text = action["text"]
    keyboard.write(text, delay=0.02)


def _perform_key(action: Dict[str, Any]):
    keys = action["keys"]
    keyboard.press_and_release(keys)


ACTION_DISPATCH = {
    "click": _perform_click,
    "type": _perform_type,
    "key": _perform_key,
}


def execute_actions(actions: List[Dict[str, Any]]):
    for act in actions:
        act_type = act.get("type")
        fn = ACTION_DISPATCH.get(act_type)
        if not fn:
            print(f"[WARN] Unknown action type: {act_type}")
            continue
        fn(act)
        time.sleep(0.3)  # brief pause between actions