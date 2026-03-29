import os





def find_project_root(current_path, marker="archive"):
    """
    Locate the root directory of the project by searching upward
    from the current file location.

    Walks up the directory tree until finds the folder
    with specific marker (e.g., "archive"), assumed
    to indicate the project root.

    Parameters:
        current_path (str): Path to the current file (__file__)
        marker (str): Name of a directory or file that identifies
                      the project root (default: "archive")

    Returns:
        str: Absolute path to the project root directory

    Raises:
        FileNotFoundError: If the project root cannot be found
    """






    # Convert to absolute path in case a relative path is provided
    current_dir = os.path.abspath(os.path.dirname(current_path))



    while True:
        # Check if the marker directory exists in the current directory
        if marker in os.listdir(current_dir):
            return current_dir


        # Move one level up in the directory tree
        parent_dir = os.path.dirname(current_dir)


        # If reached the filesystem root, stop searching
        if parent_dir == current_dir:
            raise FileNotFoundError(
                f"Project root not found. '{marker}' directory does not exist in any parent directories."
            )

        current_dir = parent_dir