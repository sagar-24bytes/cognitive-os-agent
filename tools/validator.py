from tools.registry import ALLOWED_TOOLS
from tools.normalizer import TOOL_MAPPING

def validate_plan_node(state):
    plan = state["plan"]
    validated_steps = []

    for step in plan.get("steps", []):
        tool = step.get("tool")

        # Normalize tool name
        if tool in TOOL_MAPPING:
            tool = TOOL_MAPPING[tool]
            step["tool"] = tool

        if tool not in ALLOWED_TOOLS:
            print(f"Unknown tool: {tool}, skipping")
            continue

        validated_steps.append(step)

    plan["steps"] = validated_steps
    return {"plan": plan}
