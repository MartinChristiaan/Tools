# argparse input to xlsx
# output class

import pandas as pd
import pyperclip


def generate_class_from_csv_or_excel(file_path, class_name="GeneratedDataFrame"):
    # Load the CSV or Excel file into a Pandas DataFrame
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xls"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and XLSX are supported.")

    # Generate Python class string
    class_string = f"""
class {class_name}(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super({class_name}, self).__init__(*args, **kwargs)

{indent(create_properties(df), spaces=4)}
"""

    return class_string


def create_properties(df):
    properties = []
    for column in df.columns:
        properties.append(f"@property")
        properties.append(f"def {column}(self):")
        properties.append(f"	return '{column}'")
        properties.append("")
    return "\n".join(properties)


def indent(text, spaces):
    lines = text.split("\n")
    indented_lines = [f"{' ' * spaces}{line}" for line in lines]
    return "\n".join(indented_lines)


# Example usage
file_path = "2023.xls"  # Provide the path to your CSV or XLSX file
class_name = "BudgetDF"  # Provide a desired class name

class_code = generate_class_from_csv_or_excel(file_path, class_name)
print(class_code)
pyperclip.copy(class_code)
