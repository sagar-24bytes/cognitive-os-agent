from voice.input import listen
from planner.graph import build_planner_graph
from langchain_core.messages import HumanMessage

planner_graph = build_planner_graph()

def main():
    print("Personal Cognitive OS booting...")

    user_text = listen()
    print("Heard:", user_text)

    result = planner_graph.invoke({
        "messages": [HumanMessage(content=user_text)],
        "user_text": user_text,
        "plan": {}
    })

    print("\nGenerated Plan:")
    print(result["plan"])

if __name__ == "__main__":
    main()
