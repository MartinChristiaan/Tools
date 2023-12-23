# home = os.path.expanduser('~')
from pathlib import Path

import pkg_resources


def get_installed_package_folders():
    """
    Get the folders of all installed and accessible Python packages.

    Returns:
            A list of folder paths where packages are installed.
    """
    package_folders = []

    for package in pkg_resources.working_set:
        if hasattr(package, "location"):
            package_folders.append(f"{package.location}/{package.project_name}")
    return package_folders


def get_python_files(path):
    return list(Path(path).rglob("**/*.py"))


import ast


def get_functions_with_details_from_file(file_path):
    """
    Extracts function details including parent class, arguments, and return info from a Python file.

    Args:
            file_path (str): The path to the Python file.

    Returns:
            list: A list of dictionaries, each containing information about a function.
                      Each dictionary has 'name', 'class' (parent class), 'args' (list of argument names),
                      and 'returns' (return type) keys.
    """
    functions = []

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
        tree = ast.parse(text)
        lines = text.split("\n")

    current_class = None  # To keep track of the current class

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            print(lines[node.lineno - 1])

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            print(lines[node.lineno - 1])
            # function_info = {"name": node.name, "class": current_class}
            # # Extract function arguments
            # args = [arg.arg for arg in node.args.args]
            # function_info["args"] = args

            # # Extract return type if present
            # function_info["returns"] = node.returns

            # functions.append(function_info)

    return functions


# Example usage:
if __name__ == "__main__":
    installed_package_folders = get_installed_package_folders()
    # print(get_installed_package_folders())
    folder = "/usr/lib/python3/dist-packages/colorama"
    files = get_python_files(folder)
    print(files)
    get_functions_with_details_from_file(
        "/home/martin/personal_git/imagedb/database/vector_database.py"
    )

    # git_folders = [x for x in Path(f'{home}/git').glob("*") if x.is_dir()]
