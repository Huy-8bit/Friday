from __future__ import annotations

import sys
import time
import json
from typing import List, Dict, Any

from eye import capture_screen
from brain import plan_actions
from executor import execute_actions, click_history
from utils import try_open_local_app

# Trí nhớ hội thoại giữa user và agent
chat_history: List[Dict[str, str]] = []

MAX_RETRIES = 3


def loop_agent():
    print("Conversational GUI Agent ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("🧠 You> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            sys.exit(0)

        if try_open_local_app(user_input):
            continue

        chat_history.append({"role": "user", "parts": user_input})

        step = 1
        prev_actions: List[Dict[str, Any]] = []
        retries = 0

        while True:
            print(f"[STEP {step}] Capturing screen…")
            b64_image, _ = capture_screen()

            if click_history:
                failed_coords = ", ".join(f"({x},{y})" for x, y in click_history)
                chat_history.append({
                    "role": "user",
                    "parts": f"I already tried clicking these positions and it failed: {failed_coords}"
                })

            try:
                actions = plan_actions(chat_history, b64_image)
            except Exception as e:
                print(f"[ERROR] Planning failed: {e}")
                break

            if not actions:
                print("[DONE] No more actions needed.")
                break

            if actions == prev_actions:
                retries += 1
                if retries >= MAX_RETRIES:
                    print("[WARN] Agent is stuck in a loop with same actions. Stopping.")
                    break
                print(f"[RETRY] Same actions as before. Retrying… ({retries}/{MAX_RETRIES})")
            else:
                retries = 0

            print("[PLAN]", json.dumps(actions, indent=2, ensure_ascii=False))
            execute_actions(actions)
            prev_actions = actions
            time.sleep(1)
            step += 1

        chat_history.append({"role": "model", "parts": "Actions executed."})


if __name__ == "__main__":
    loop_agent()
