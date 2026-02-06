# planner/intent.py

def classify_intent(user_text: str) -> str:
    text = user_text.lower().strip()

    ORGANIZE = [
        "organize", "sort", "arrange", "cleanup", "clean up"
    ]
    OPEN = [
        "open", "launch", "show"
    ]
    SEARCH = [
        "search", "find", "look for"
    ]
    CREATE = [
        "create", "make", "new"
    ]

    for word in ORGANIZE:
        if word in text:
            return "organize"

    for word in OPEN:
        if word in text:
            return "open"

    for word in SEARCH:
        if word in text:
            return "search"

    for word in CREATE:
        if word in text:
            return "create"

    return "unknown"
