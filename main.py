from voice.input import listen
from planner.graph import build_planner_graph
from langchain_core.messages import HumanMessage
from planner.intent import classify_intent
from tools.actions import open_folder
from memory.path_resolver import resolve_path_from_text
from memory.context import context  


planner_graph = build_planner_graph()


def main():
    print("Personal Cognitive OS booting...")

    # ===============================
    # 🎙️ PERCEPTION
    # ===============================
    user_text = listen()
    print("Heard:", user_text)

    # ===============================
    # 🧠 INTENT CLASSIFICATION
    # ===============================
    intent = classify_intent(user_text)
    print(f"[Intent] {intent}")

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
            return

        open_folder(path)
        return

    # ===============================
    # 🧩 PLANNING + EXECUTION
    # ===============================
    result = planner_graph.invoke({
        "messages": [HumanMessage(content=user_text)],
        "user_text": user_text,
        "intent": intent,
        "plan": {}
    })

    print("\nGenerated Plan:")
    print(result.get("plan"))


if __name__ == "__main__":
    main()
