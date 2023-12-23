import ast


def get_defined_classes_functions(module_path):
    defined_classes = []
    defined_functions = []

    with open(module_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=module_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            defined_functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            defined_classes.append(node.name)

    return defined_classes, defined_functions


def find_imported_modules(script_path):
    imported_modules = set()
    with open(script_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=script_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                for alias in node.names:
                    imported_modules.add(f"{module_name}.{alias.name}")
    return imported_modules


def detect_classes_functions(script_path):
    defined_classes, defined_functions = get_defined_classes_functions(script_path)
    imported_modules = find_imported_modules(script_path)

    print(f"User-defined classes in {script_path}:")
    for class_name in defined_classes:
        print(class_name)

    print(f"\nUser-defined functions in {script_path}:")
    for function_name in defined_functions:
        print(function_name)

    print(f"\nImported modules in {script_path}:")
    for module_name in imported_modules:
        print(module_name)


if __name__ == "__main__":
    script_path = "/home/leeuwenmcv/git/dlutils_ii/dlutils_ii/ii_dataset.py"  # Replace with the path to your Python script
    detect_classes_functions(script_path)
