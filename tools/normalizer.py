TOOL_MAPPING = {
    "list_files": "scan_folder",
    "categorize_files": "scan_folder",
    "create_folders": "create_folder",
    "create_directory": "create_folder",
    "move_files": "move_file",
    "filter_files": "move_file",  # fallback
}

ARG_MAPPING = {
    "create_folder": {
        "folder_name": "path",
        "directory": "path"
    },
    "scan_folder": {
        "directory": "path"
    },
    "move_file": {
        "source_files": "source_directory",
        "directory": "source_directory",
        "dest": "destination_directory",
        "pattern": "file_pattern"
    }
}
