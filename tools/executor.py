def execute_plan_node(state):
    plan = state["plan"]

    print("\n--- DRY RUN EXECUTION ---")

    for i, step in enumerate(plan.get("steps", []), 1):
        tool = step["tool"]
        args = step["args"]
        print(f"Step {i}: Would execute {tool} with args {args}")

    print("--- END DRY RUN ---\n")

    return {}
