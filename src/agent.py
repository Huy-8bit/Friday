from __future__ import annotations

import json
import sys
import time
from typing import List, Dict, Any

from eye import capture_screen
from brain import plan_actions
from hand import execute_actions
from utils import try_open_local_app

def loop_until_done(user_cmd: str, max_steps: int = 5):
    for step in range(max_steps):
        print(f"[STEP {step+1}] Capturing screen…")
        b64_image, _ = capture_screen()
        try:
            actions = plan_actions(b64_image, user_cmd)
        except Exception as e:
            print(f"[ERROR] {e}")
            break

        if not actions:
            print("[DONE] No more actions needed.")
            break

        print("[PLAN]", json.dumps(actions, indent=2, ensure_ascii=False))
        execute_actions(actions)
        time.sleep(1)

def main():
    print("Vision GUI Agent started. Type 'exit' to quit.\n")
    while True:
        user_cmd = input("👉 Command> ").strip()
        if user_cmd.lower() in {"exit", "quit"}:
            print("Bye!")
            sys.exit(0)

        if try_open_local_app(user_cmd):
            continue

        loop_until_done(user_cmd)

if __name__ == "__main__":
    main()
