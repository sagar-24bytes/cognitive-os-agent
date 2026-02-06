import os
from memory.context import context


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

    # -------------------------------------------------
    # 1️⃣ Explicit semantic resolution (authoritative)
    # -------------------------------------------------
    for key, path in KNOWN_FOLDERS.items():
        if key in text:
            resolved = os.path.abspath(path)
            context.last_path = resolved  # ✅ store safely
            return resolved

    # -------------------------------------------------
    # 2️⃣ Memory fallback (ONLY when explicitly needed)
    # -------------------------------------------------
    return getattr(context, "last_path", None)
