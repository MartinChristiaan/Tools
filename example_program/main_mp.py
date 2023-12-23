import argparse
from dataclasses import dataclass

from tqdm import tqdm

from utils.dataframe_utils import load_config, map_multiprocessed


@dataclass
class ExampleArgClass:
    name: str
    age: int
    number: float

    @staticmethod
    def from_df(df):
        return [ExampleArgClass(**row) for i, row in df.iterrows()]


def action(person):
    print(person)


def main():
    parser = argparse.ArgumentParser(
        prog="ExampleProgram", description="ExampleDescription"
    )
    parser.add_argument("-c", "--config", type=str, default="config/default.csv")
    parser.add_argument("-q", "--query", type=str, default="config/query_all.py")
    args = parser.parse_args()
    updated_df = load_config(ExampleArgClass, args.config, args.query)
    persons = ExampleArgClass.from_df(updated_df)
    map_multiprocessed(action, persons)


if __name__ == "__main__":
    main()
