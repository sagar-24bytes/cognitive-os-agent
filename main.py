from voice.input import listen
from planner.graph import build_planner_graph
from langchain_core.messages import HumanMessage
from planner.intent import classify_intent
from tools.actions import open_folder
from memory.path_resolver import resolve_path_from_text
from memory.context import context


planner_graph = build_planner_graph()


def is_noise(text: str) -> bool:
    """
    Returns True if input is only filler / punctuation noise
    e.g. '.', '...', ',,,'
    """
    stripped = text.strip()
    if not stripped:
        return True
    return all(c in "., " for c in stripped)


def main():
    print("🧠 Personal Cognitive OS booted. Say something…")

    awaiting_open_target = False

    while True:
        # ===============================
        # 🎙️ PERCEPTION
        # ===============================
        user_text = listen()

        if not user_text:
            print("…")
            continue

        user_text = user_text.strip()

        # ---- NOISE FILTER (CRITICAL FIX) ----
        if is_noise(user_text):
            print("…")
            continue

        print("Heard:", user_text)

        # ===============================
        # 🔚 EXIT CONDITION
        # ===============================
        normalized = user_text.lower().rstrip(".!")
        if normalized in {"exit", "quit", "stop", "bye"}:
            print("👋 Shutting down Cognitive OS.")
            break

        # ===============================
        # 🧠 INTENT CLASSIFICATION
        # ===============================
        intent = classify_intent(user_text)
        print(f"[Intent] {intent}")

        # ===============================
        # NO-ACTION / CHITCHAT
        # ===============================
        if intent == "no_action":
            print("🙂 Got it.")
            continue


        # ===============================
        # 🧩 CLARIFICATION CONTINUATION
        # ===============================
        if awaiting_open_target:
            path = resolve_path_from_text(user_text)

            if path:
                open_folder(path)
                awaiting_open_target = False
                continue

            print("❓ I still couldn’t identify the folder.")
            continue

        # ===============================
        # 📂 DIRECT ACTION: OPEN FOLDER
        # ===============================
        if intent == "open":
            path = resolve_path_from_text(user_text)

            # 🧠 memory fallback
            if not path:
                path = getattr(context, "last_path", None)

            if not path:
                print("❓ Which folder should I open?")
                awaiting_open_target = True
                continue

            open_folder(path)
            continue

        # ===============================
        # 🧩 PLANNING + EXECUTION
        # ===============================
        try:
            result = planner_graph.invoke({
                "messages": [HumanMessage(content=user_text)],
                "user_text": user_text,
                "intent": intent,
                "plan": {}
            })

            print("\nGenerated Plan:")
            print(result.get("plan"))

        except Exception as e:
            print("⚠️ Error during execution:", e)


if __name__ == "__main__":
    main()
