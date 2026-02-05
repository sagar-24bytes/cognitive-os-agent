import os
import re

KNOWN_FOLDERS = {
    "agent test folder": "B:/agent_test",
    "agent_test": "B:/agent_test",
    "downloads": os.path.expanduser("~/Downloads"),
    "documents": os.path.expanduser("~/Documents"),
}

def resolve_path_from_text(text: str | None):
    if not text:
        return None

    text = text.lower().strip()

    # Exact semantic matches first
    for key, path in KNOWN_FOLDERS.items():
        if key in text:
            return os.path.abspath(path)

    # If no known folder is mentioned, DO NOT guess
    return None
