# planner/intent.py

def classify_intent(user_text: str | None) -> str:
    if not user_text:
        return "no_action"

    text = user_text.lower().strip().rstrip(".!?,")

    # ===============================
    # 🔚 EXIT INTENT
    # ===============================
    normalized = text.rstrip(".!?,")
    EXIT_WORDS = {"exit", "quit", "stop", "bye"}

    if any(word in normalized.split() for word in EXIT_WORDS):
        return "exit"

    # ===============================
    # 🎯 ACTION INTENTS (CHECK FIRST)
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
    # 😶 NO-ACTION / CHITCHAT
    # ===============================
    NO_ACTION_PHRASES = {
        "thank you",
        "thanks",
        "ok",
        "thank you.",
        "thanks.",
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

    if text in NO_ACTION_PHRASES:
        return "no_action"

    # ===============================
    # ❓ FALLBACK
    # ===============================
    return "unknown"