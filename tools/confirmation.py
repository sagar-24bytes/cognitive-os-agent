# tools/confirmation.py

from voice.input import listen


def confirmation_node(state):
    plan = state.get("plan", {})
    steps = plan.get("steps", [])

    if not steps:
        print("Nothing to execute.")
        state["approved"] = False
        return state

    print("\n--- PLAN PREVIEW ---")

    affected_paths = set()

    for step in steps:
        tool = step["tool"]
        args = step["args"]

        if "path" in args:
            affected_paths.add(args["path"])

        if "source_directory" in args:
            affected_paths.add(args["source_directory"])

        if "destination_directory" in args:
            affected_paths.add(args["destination_directory"])

        print(f"- {tool} {args}")

    print("\nAffected locations:")
    for p in affected_paths:
        print(f"  {p}")

    print("\nSay or type YES to proceed, NO to cancel")

    # Try voice confirmation first
    try:
        print("Listening for confirmation...")
        answer = listen().lower().strip().rstrip(".!?,")
        print("Heard:", answer)
    except:
        answer = ""

    # Fallback to keyboard if empty
    if not answer:
        answer = input("Proceed? (yes/no): ").strip().lower().rstrip(".!?,")

    if answer in ("yes", "y"):
        state["approved"] = True
    else:
        state["approved"] = False
        print("Execution cancelled.")

    return state