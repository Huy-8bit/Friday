# =========================
# File: executor.py
# -------------------------
from __future__ import annotations

import time
import sys
from typing import Dict, Any, List

import pyautogui
import psutil

# === Action Handlers ===
click_history: List[tuple[int, int]] = []

def is_app_running(app: str) -> bool:
    return any(app.lower() in (p.name().lower() or '') for p in psutil.process_iter())

def act_click(action: Dict[str, Any]):
    x = int(action["x"])
    y = int(action["y"])
    print(f"[EXEC] Click at ({x}, {y})")
    click_history.append((x, y))
    pyautogui.moveTo(x, y, duration=0.15)
    pyautogui.click()

def act_type(action: Dict[str, Any]):
    text = action["text"]
    print(f"[EXEC] Typing: {text}")
    pyautogui.typewrite(text, interval=0.02)

def act_key(action: Dict[str, Any]):
    keys = action["keys"]
    if isinstance(keys, str):
        keys = keys.lower().replace("cmd", "command").split("+")
    print(f"[EXEC] Pressing key combo: {keys}")
    pyautogui.hotkey(*keys)

def act_open_app(action: Dict[str, Any]):
    app = action["app"].lower()
    print(f"[EXEC] Opening app like a user: {app}")

    if "chrome" in app:
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.typewrite("chrome", interval=0.05)
        time.sleep(0.3)
        pyautogui.press("enter")
    elif "notepad" in app:
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.typewrite("notepad", interval=0.05)
        time.sleep(0.3)
        pyautogui.press("enter")
    elif "music" in app:
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.typewrite("apple music", interval=0.05)
        time.sleep(0.3)
        pyautogui.press("enter")
    else:
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.typewrite(app, interval=0.05)
        time.sleep(0.3)
        pyautogui.press("enter")

def act_wait(action: Dict[str, Any]):
    secs = float(action.get("seconds", 1))
    print(f"[EXEC] Waiting {secs} seconds…")
    time.sleep(secs)

# === Dispatcher ===
ACTION_MAP = {
    "click": act_click,
    "type": act_type,
    "key": act_key,
    "open_app": act_open_app,
    "wait": act_wait,
}

def execute_actions(actions: List[Dict[str, Any]]):
    for act in actions:
        action_type = act.get("type")
        fn = ACTION_MAP.get(action_type)
        if fn:
            fn(act)
            time.sleep(0.2)
        else:
            print(f"[WARN] Unknown action type: {action_type}")