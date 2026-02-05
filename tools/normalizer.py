TOOL_MAPPING = {
    "list_files": "scan_folder",
    "categorize_files": "scan_folder",
    "create_folders": "create_folder",
    "create_directory": "create_folder",
    "move_files": "move_file",
    "filter_files": "move_file",  # fallback
}

ARG_MAPPING = {
    "scan_folder": {
        "folder_path": "path",
        "directory": "path",
        "path": "path",
    },
    "create_folder": {
        "folder_path": "path",
        "directory": "path",
        "path": "path",
    },
    "move_file": {
        "source_path": "source_directory",
        "source_directory": "source_directory",
        "destination_path": "destination_directory",
        "destination_directory": "destination_directory",
        "pattern": "file_pattern",
        "file_pattern": "file_pattern",
    }
}


