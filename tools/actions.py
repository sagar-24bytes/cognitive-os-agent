import os
import shutil
from pathlib import Path

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
    import glob, shutil, os

    source_directory = os.path.abspath(os.path.expanduser(source_directory))
    destination_directory = os.path.abspath(os.path.expanduser(destination_directory))

    files = glob.glob(os.path.join(source_directory, file_pattern))

    if not files:
        print(f"No files found matching {file_pattern}")
        return  # <--- THIS LINE IS THE IMPORTANT PART

    os.makedirs(destination_directory, exist_ok=True)

    for f in files:
        shutil.move(f, destination_directory)
        print(f"Moved {os.path.basename(f)} → {destination_directory}")



