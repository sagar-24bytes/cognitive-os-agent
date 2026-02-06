import os
import shutil
from pathlib import Path
import fnmatch

def resolve_path(path):
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path

def scan_folder(path):
    path = resolve_path(path)
    files = os.listdir(path)
    print(f"Scanned {path}: {len(files)} files found")
    return files

def create_folder(path, categories=None):
    path = resolve_path(path)
    if categories:
        for cat in categories:
            folder_path = os.path.join(path, cat)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created folder: {folder_path}")
    else:
        os.makedirs(path, exist_ok=True)
        print(f"Created folder: {path}")



def move_file(source_directory, destination_directory, file_pattern):
    source_directory = os.path.abspath(os.path.expanduser(source_directory))
    destination_directory = os.path.abspath(os.path.expanduser(destination_directory))

    # 🔧 FINAL POLISH: sanitize pattern from LLM / speech noise
    file_pattern = "".join(file_pattern.split()).lower()

    files = [
        f for f in os.listdir(source_directory)
        if os.path.isfile(os.path.join(source_directory, f))
        and fnmatch.fnmatch(f.lower(), file_pattern)
    ]

    if not files:
        print(f"No files found matching {file_pattern}")
        return

    os.makedirs(destination_directory, exist_ok=True)

    for f in files:
        shutil.move(
            os.path.join(source_directory, f),
            os.path.join(destination_directory, f)
        )
        print(f"Moved {f} → {destination_directory}")
def open_folder(path):
    import os
    path = os.path.abspath(os.path.expanduser(path))

    if not os.path.exists(path):
        print(f"Folder not found: {path}")
        return

    os.startfile(path)
    print(f"Opened folder: {path}")










