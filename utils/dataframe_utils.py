import importlib.util
import multiprocessing
import os
from dataclasses import fields
from pathlib import Path

import click
import pandas as pd
from tqdm import tqdm

from utils.SFzfPrompt import SFzfPrompt


def load_config(dataclass, csv_path, query_file_path):
    df = update_csv_with_dataclass(dataclass, csv_path)
    return run_query(df, Path(query_file_path))


def map_multiprocessed(action, persons):
    num_processes = multiprocessing.cpu_count()  # Use all available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)
    tqdm(pool.imap(action, persons), total=len(persons))
    pool.close()
    pool.join()


def create_config_csv(csv_path, dataclass):
    headers = [field.name for field in fields(dataclass)]
    df = pd.DataFrame(columns=headers)
    df.to_csv(csv_path, index=False)
    print(f"CSV file created with headers from {dataclass.__name__}.")
    os.system(f"xdg-open {csv_path}")
    return df


def update_csv_with_dataclass(dataclass, csv_path):
    # Check if the CSV file exists
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        # CSV file doesn't exist, create it with headers from dataclass
        headers = [field.name for field in fields(dataclass)]
        df = pd.DataFrame(columns=headers)
        df.to_csv(csv_path, index=False)
        print("CSV file created with headers from dataclass.")
        print("Opening the CSV file...")
        # open_csv_file(csv_path)
        df = pd.read_csv(csv_path)
        return df
    # Check if CSV headers match dataclass fields
    existing_headers = df.columns.tolist()
    expected_headers = [field.name for field in fields(dataclass)]

    if existing_headers != expected_headers:
        missing_headers = [
            header for header in expected_headers if header not in existing_headers
        ]
        extra_headers = [
            header for header in existing_headers if header not in expected_headers
        ]
        prompt = SFzfPrompt()

        for header in missing_headers:
            print(f"fill {header} ? y/n")
            if not click.getchar() == "y":
                df[header] = None
                continue
            fill_header = prompt.prompt(
                extra_headers, False, f"select header for {header}"
            )
            df[header] = df[fill_header]
        print(df)
        df = df.drop(columns=extra_headers)
        # df = df.reindex(columns=expected_headers, fill_value=None)
        print("df file headers updated to match dataclass.")
        print("The DataFrame:")
        print(df.to_markdown())

        if confirm_changes():
            df.to_csv(csv_path, index=False)
            print("CSV file updated successfully.")
        else:
            print("No changes were saved.")
    else:
        print("df is up to date")
    return df


def import_module_from_path(module_path):
    module_path = str(module_path)
    module_name = module_path.split("/")[-1].split(".")[0]  # Extract module name
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sample_file = """
import pandas as pd
def query(df:pd.DataFrame):
	return df
"""


def run_query(df, query_file: Path):
    if not query_file.exists():
        with open(query_file, "w") as f:
            f.write(sample_file)
    imported_module = import_module_from_path(query_file)
    df = imported_module.query(df)
    return df


def confirm_changes():
    print("Do you want to save the changes? (y/n): ")
    char = click.getchar()
    return char == "y"


def open_csv_file(csv_path):
    try:
        import subprocess

        subprocess.run(["xdg-open", csv_path])
    except Exception as e:
        print("Error opening the CSV file:", e)


# Example usage
if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass
    class Person:
        name: str
        age: int
        number: float

        @staticmethod
        def from_df(df):
            return [Person(**row) for i, row in df.iterrows()]

    csv_file_path = "people.csv"
    updated_df = update_csv_with_dataclass(Person, csv_file_path)
    persons = Person.from_df(updated_df)
    print(persons)
