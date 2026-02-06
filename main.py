from planner import intent
from voice.input import listen
from planner.graph import build_planner_graph
from langchain_core.messages import HumanMessage
from planner.intent import classify_intent
from tools.actions import open_folder
from memory.path_resolver import resolve_path_from_text


planner_graph = build_planner_graph()

def main():
    print("Personal Cognitive OS booting...")

    user_text = listen()
    print("Heard:", user_text)
    intent = classify_intent(user_text)
    print(f"[Intent] {intent}")
    

    if intent == "open":
        path = resolve_path_from_text(user_text)
        open_folder(path)
        return



    result = planner_graph.invoke({
    "messages": [HumanMessage(content=user_text)],
    "user_text": user_text,
    "intent": intent,
    "plan": {}
    })


    print("\nGenerated Plan:")
    print(result["plan"])

if __name__ == "__main__":
    main()
