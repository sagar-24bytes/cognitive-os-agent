from tools.actions import scan_folder, create_folder, move_file

TOOL_FUNCTIONS = {
    "scan_folder": scan_folder,
    "create_folder": create_folder,
    "move_file": move_file
}

def execute_plan_node(state):
    plan = state["plan"]

    print("\n--- REAL EXECUTION ---")

    for i, step in enumerate(plan.get("steps", []), 1):
        tool = step["tool"]
        args = step["args"]

        if tool in TOOL_FUNCTIONS:
            try:
                print(f"Step {i}: Executing {tool} with args {args}")
                TOOL_FUNCTIONS[tool](**args)
            except TypeError as e:
                print(f"Argument mismatch for {tool}: {e}")
        else:
            print(f"Unknown tool: {tool}")

    print("--- END EXECUTION ---\n")
    return {}
