import os

def find_project_root(start_path, marker=".git"): 
    path = os.path.abspath(start_path)
    while True:
        if os.path.isdir(os.path.join(path, marker)):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            raise RuntimeError(f"Cannot find project root with marker '{marker}'")
        path = parent