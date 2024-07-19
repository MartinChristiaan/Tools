import importlib


def run_module(module_name):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, "__main__"):
            module.__main__()
        else:
            print(f"Module {module_name} doesn't have a __main__ function.")
    except ImportError:
        print(f"Module {module_name} not found.")


# Example usage:
if __name__ == "__main__":
    run_module("another_module")
