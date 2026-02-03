KNOWN_PATHS = {
    "agent test": "B:/agent_test",
    "downloads": "~/Downloads",
    "desktop": "~/Desktop",
    "documents": "~/Documents"
}

def resolve_path_from_text(user_text):
    user_text = user_text.lower()
    for name, path in KNOWN_PATHS.items():
        if name in user_text:
            return path
    return None
