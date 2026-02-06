from tools.registry import ALLOWED_TOOLS
from tools.normalizer import TOOL_MAPPING, ARG_MAPPING
from memory.path_resolver import resolve_path_from_text
import os


def validate_plan_node(state):
    plan = state["plan"]
    user_text = state["user_text"]
    validated_steps = []

    resolved_path = resolve_path_from_text(user_text)

    # 🚨 HARD STOP: no path, no file ops
    if not resolved_path:
        print("❓ No folder resolved — skipping execution")
        plan["steps"] = []
        return {"plan": plan}

    # =================================================
    # 🌍 WORLD MODEL RESOLUTION (AUTHORITATIVE PATH)
    # =================================================
    

    for step in plan.get("steps", []):
        tool = step.get("tool")
        args = step.get("args", {}).copy()

        # ---- REMOVE SYMBOLIC / TEMPLATE VARIABLES ----
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

        # =================================================
        # 🔒 PATH GROUNDING — SINGLE SOURCE OF TRUTH
        # =================================================
        if resolved_path:
            if tool in ("scan_folder", "create_folder"):
                args["path"] = resolved_path

            elif tool == "move_file":
                args["source_directory"] = resolved_path

        # =================================================
        # 🧠 AUTO FILE-TYPE ORGANIZATION (FINAL, CORRECT)
        # =================================================
        if tool == "move_file":
            src = resolved_path

            file_groups = {
                "*.pdf": "documents",
                "*.png": "images",
                "*.jpg": "images",
                "*.jpeg": "images",
                "*.mp4": "videos",
                "*.mkv": "videos",
            }

            # ---- typed moves ----
            for pattern, folder in file_groups.items():
                dest = os.path.join(src, folder)

                validated_steps.append({
                    "tool": "create_folder",
                    "args": {"path": dest}
                })

                validated_steps.append({
                    "tool": "move_file",
                    "args": {
                        "source_directory": src,
                        "destination_directory": dest,
                        "file_pattern": pattern
                    }
                })

            # ---- FINAL POLISH: fallback only if files remain ----
            remaining_files = [
                f for f in os.listdir(src)
                if os.path.isfile(os.path.join(src, f))
            ]

            if remaining_files:
                other_dest = os.path.join(src, "others")

                validated_steps.append({
                    "tool": "create_folder",
                    "args": {"path": other_dest}
                })

                validated_steps.append({
                    "tool": "move_file",
                    "args": {
                        "source_directory": src,
                        "destination_directory": other_dest,
                        "file_pattern": "*"
                    }
                })

            # IMPORTANT: do not add original move_file step
            continue

        # =================================================
        # 🚫 SKIP USELESS ROOT RECREATION
        # =================================================
        if tool == "create_folder" and args.get("path") == resolved_path:
            continue

        validated_steps.append({
            "tool": tool,
            "args": args
        })

    # =================================================
    # ♻️ DEDUPLICATION
    # =================================================
    unique_steps = []
    seen = set()

    for step in validated_steps:
        key = (step["tool"], tuple(sorted(step["args"].items())))
        if key not in seen:
            seen.add(key)
            unique_steps.append(step)

    plan["steps"] = unique_steps
    return {"plan": plan}
