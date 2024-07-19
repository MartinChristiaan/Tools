import ast
import re


def extract_import_statements(file_contents):
    # Define a regular expression pattern to match import statements
    pattern = r"^\s*(import\s+[\w, ]+|\bfrom\s+[\w.]+\s+import\s+[\w, ]+|\bimport\s+[\w.]+\s+as\s+[\w, ]+)"

    # Use re.findall to extract import statements
    import_statements = re.findall(pattern, file_contents, re.MULTILINE)

    # Join the matched import statements into a single string
    import_string = "\n".join(import_statements)

    return import_string


def extract_functions_with_generate_docstring(parsed_tree):
    # Parse the input code into an abstract syntax tree (AST)

    # Create a list to store functions with "generate" in their docstring
    functions_with_generate_docstring = []

    # Helper function to check if a docstring contains the word "generate"
    def contains_generate(word):
        return "generate" in word.lower()

    # Traverse the AST and extract functions with the desired docstring
    for node in ast.walk(parsed_tree):
        if isinstance(node, ast.FunctionDef):
            if node.name.startswith("genme_"):
                functions_with_generate_docstring.append(node)
    return functions_with_generate_docstring


# Example usage
if __name__ == "__main__":
    with open("example_input.py", "r") as file:
        python_code = file.read()

    parsed_tree = ast.parse(python_code)
    functions = extract_functions_with_generate_docstring(parsed_tree)
    imports = extract_import_statements(python_code)
    for fn in functions:
        body = ast.unparse(fn).replace("genme_", "")
        statment = "finish to following python function: \n" + imports + "\n" + body
        print(statment)
        # network_input =
    # print("Functions with 'generate' in their docstring:", function_names)


# # Example usage
# if __name__ == "__main__":
#     with open('your_python_file.py', 'r') as file:
#         python_code = file.read()

#     import_statements = extract_import_statements(python_code)
#     print(import_statements)
