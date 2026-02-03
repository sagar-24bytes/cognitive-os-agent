from langgraph.graph import StateGraph, START, END
from planner.state import AgentState
from planner.planner import planner_node
from tools.validator import validate_plan_node

def build_planner_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("validator", validate_plan_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "validator")
    graph.add_edge("validator", END)

    return graph.compile()
