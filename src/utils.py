# =========================
# File: utils.py
# -------------------------
import subprocess

WHITELISTED_APPS = {
    "notes": "Notes",
    "textedit": "TextEdit",
    "chrome": "Google Chrome",
    "finder": "Finder",
    "safari": "Safari",
    "terminal": "Terminal",
}

def try_open_local_app(command: str) -> bool:
    """
    Nếu command có chứa yêu cầu mở app hợp lệ, thì mở app đó và trả True.
    Ngược lại trả False để xử lý bằng GPT như bình thường.
    """
    for key in WHITELISTED_APPS:
        if f"open {key}" in command.lower() or f"mở {key}" in command.lower():
            app_name = WHITELISTED_APPS[key]
            print(f"[INFO] Opening app: {app_name}")
            subprocess.run(["open", "-a", app_name])
            return True
    return False
