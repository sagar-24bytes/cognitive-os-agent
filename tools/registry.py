# tools/registry.py

from tools.actions import (
    scan_folder,
    create_folder,
    move_file,
    open_folder,
)

# 🔒 Single source of truth for allowed tools
ALLOWED_TOOLS = {
    "scan_folder",
    "create_folder",
    "move_file",
    "open_folder",
}

# 🧰 Tool name → function mapping used by executor
TOOL_FUNCTIONS = {
    "scan_folder": scan_folder,
    "create_folder": create_folder,
    "move_file": move_file,
    "open_folder": open_folder,
}
