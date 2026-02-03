from tools.registry import ALLOWED_TOOLS
from tools.normalizer import TOOL_MAPPING, ARG_MAPPING
from memory.path_resolver import resolve_path_from_text


def validate_plan_node(state):
    plan = state["plan"]
    user_text = state["user_text"]
    validated_steps = []

    # ---- WORLD MODEL RESOLUTION ----
    resolved_path = resolve_path_from_text(user_text)

    for step in plan.get("steps", []):
        tool = step.get("tool")
        args = step.get("args", {})

        # ---- REMOVE SYMBOLIC / FAKE VARIABLES ----
        for k, v in list(args.items()):
            if isinstance(v, str) and "{{" in v:
                del args[k]

        # ---- TOOL NORMALIZATION ----
        if tool in TOOL_MAPPING:
            tool = TOOL_MAPPING[tool]

        # ---- TOOL GROUNDING ----
        if tool not in ALLOWED_TOOLS:
            print(f"Unknown tool: {tool}, skipping")
            continue

        # ---- ARG NORMALIZATION ----
        if tool in ARG_MAPPING:
            for old, new in ARG_MAPPING[tool].items():
                if old in args:
                    args[new] = args.pop(old)

        # ---- PATH GROUNDING (THIS IS THE KEY FIX) ----
        if resolved_path:
            if "path" in args:
                args["path"] = resolved_path
            if "directory" in args:
                args["directory"] = resolved_path
            if "source_directory" in args:
                args["source_directory"] = resolved_path
            if "destination_directory" in args:
                args["destination_directory"] = resolved_path

        step["tool"] = tool
        step["args"] = args
        validated_steps.append(step)

    plan["steps"] = validated_steps
    return {"plan": plan}
