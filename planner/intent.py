# planner/intent.py

def classify_intent(user_text: str | None) -> str:
    if not user_text:
        return "no_action"

    text = user_text.lower().strip()

    # ===============================
    # 🔚 EXIT INTENT
    # ===============================
    if text.rstrip(".!") in {"exit", "quit", "stop", "bye"}:
        return "exit"

    # ===============================
    # 😶 NO-ACTION / CHITCHAT
    # ===============================
    NO_ACTION_PHRASES = {
        "thank you",
        "thanks",
        "ok",
        "okay",
        "got it",
        "hmm",
        "hmmm",
        "alright",
        "cool",
        "fine",
        "nice",
        "yes",
        "yeah",
        "yep",
        "no",
        "nah",
        "...",
    }

    if text in NO_ACTION_PHRASES or len(text.split()) <= 2:
        return "no_action"

    # ===============================
    # 🎯 ACTION INTENTS
    # ===============================
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

    # ===============================
    # ❓ FALLBACK
    # ===============================
    return "unknown"
