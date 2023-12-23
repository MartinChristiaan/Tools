import argparse
import inspect
from dataclasses import is_dataclass
from glob import glob

import click

from utils.dataframe_utils import (
    create_config_csv,
    import_module_from_path,
    update_csv_with_dataclass,
)
from utils.SFzfPrompt import prompt

parser = argparse.ArgumentParser(
    prog="Config CLI", description="CLI for generating and updating configuration files"
)


def load_dataclass():
    dclass_files = glob("*dtypes.py", recursive=True)
    dataclasses = []
    for dclass_file in dclass_files:
        module = import_module_from_path(dclass_file)
        dataclasses += extract_dataclasses(module)
    names = [x.__name__ for x in dataclasses]
    index = prompt(names, return_idx=True, prompt_text="Choose dataclass")
    return dataclasses[index]


def extract_dataclasses(module):
    dataclasses = []
    for name, obj in inspect.getmembers(module):
        if is_dataclass(obj):
            dataclasses.append(obj)
    return dataclasses


def update_config():
    dataclass = load_dataclass()
    config_name = dataclass.__name__
    configs = glob(f"config/{config_name}*.csv")
    config_path = prompt(configs, prompt_text="choose config")
    update_csv_with_dataclass(dataclass, config_path)


def new_config():
    dataclass = load_dataclass()
    config_name = dataclass.__name__
    config_suffix = input("config suffix [default]")
    if config_suffix == "":
        config_suffix = "default"
    config_path = f"config/{config_name}_{config_suffix}.csv"
    create_config_csv(config_path, dataclass)


def print_actions(actions):
    for k, v in actions.items():
        print(f"{k} -> {v.__name__}")


print("What would you like to do?")
actions = {"u": update_config, "n": new_config}
print_actions(actions)


actions[click.getchar()]()
