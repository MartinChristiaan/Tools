import argparse

from dtypes import ExampleArgClass
from tqdm import tqdm

from utils.dataframe_utils import load_config


def action(args: ExampleArgClass):
    """
    Run main functionality here
    """
    print(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ExampleProgram", description="ExampleDescription"
    )
    parser.add_argument("-c", "--config", type=str, default="config/default.csv")
    parser.add_argument("-q", "--query", type=str, default="config/query_all.py")
    args = parser.parse_args()
    updated_df = load_config(ExampleArgClass, args.config, args.query)
    persons = ExampleArgClass.from_df(updated_df)
    for person in tqdm(persons):
        action(person)
