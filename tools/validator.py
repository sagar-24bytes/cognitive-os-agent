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

        # ---- TOOL SAFETY GATE ----
        if tool not in ALLOWED_TOOLS:
            print(f"Blocked unsupported tool: {tool}")
            continue

        # ---- ARG NORMALIZATION ----
        if tool in ARG_MAPPING:
            for old, new in ARG_MAPPING[tool].items():
                if old in args:
                    args[new] = args.pop(old)
        # ---- SPLIT source_path GLOB INTO DIR + PATTERN ----
        if tool == "move_file" and "source_directory" in args:
            src = args["source_directory"]
            if "*" in src:
                import os
                args["source_directory"] = os.path.dirname(src)
                args["file_pattern"] = os.path.basename(src)


        # ---- PATH GROUNDING ----
        if resolved_path:
            for key in ("path", "directory", "source_directory", "destination_directory"):
                if key in args:
                    args[key] = resolved_path

        step["tool"] = tool
        step["args"] = args
        validated_steps.append(step)
        # ---- AUTO-ORGANIZATION RULES ----
        if tool == "move_file":
            pattern = args.get("file_pattern", "")

            if pattern.endswith(".log"):
                args["destination_directory"] = os.path.join(
                    args["source_directory"], "logs"
                )

            elif pattern.endswith(".txt"):
                args["destination_directory"] = os.path.join(
                    args["source_directory"], "results"
                )

            elif pattern.endswith(".json"):
                args["destination_directory"] = os.path.join(
                    args["source_directory"], "configs"
                )


    # ---- DEDUPLICATION (CRITICAL FIX) ----
    unique_steps = []
    seen = set()

    for step in validated_steps:
        key = (step["tool"], tuple(sorted(step["args"].items())))
        if key not in seen:
            seen.add(key)
            unique_steps.append(step)

    plan["steps"] = unique_steps
    return {"plan": plan}
