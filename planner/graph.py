from langgraph.graph import StateGraph, START, END
from planner.state import AgentState
from planner.planner import planner_node
from tools.validator import validate_plan_node
from tools.confirmation import confirmation_node
from tools.executor import execute_plan_node


def build_planner_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("validator", validate_plan_node)
    graph.add_node("confirmation", confirmation_node)
    graph.add_node("executor", execute_plan_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "validator")
    graph.add_edge("validator", "confirmation")

    # conditional execution
    graph.add_conditional_edges(
        "confirmation",
        lambda state: state.get("approved", False),
        {
            True: "executor",
            False: END
        }
    )

    graph.add_edge("executor", END)

    return graph.compile()