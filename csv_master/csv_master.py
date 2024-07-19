import itertools
import os
import sys
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Any

import click
import numpy as np
import pandas as pd
import plotly.express as px
from pyfzf import pyfzf


class Mode(IntEnum):
    VIEW = 0
    SORT = 1


@dataclass
class Action:
    name: str
    action: any
    activation_key: str


def dataframe_to_string(df_cur, blue_row=None, blue_column=None):
    # Get column names
    dataframe = df_cur.copy()

    columns = dataframe.columns
    for column in columns:
        dataframe[column] = dataframe[column].apply(
            lambda x: f"{x:.2f}" if type(x) == float else str(x)
        )

    # Calculate maximum column widths
    column_widths = [
        max(len(str(column)), dataframe[column].astype(str).apply(len).max())
        for column in columns
    ]

    # Initialize the string representation with column names
    df_string = (
        " | ".join(
            [f"{column:{width}}" for column, width in zip(columns, column_widths)]
        )
        + "\n"
    )

    # Create a separator line
    separator = "+".join(["-" * (width + 1) for width in column_widths])
    df_string += separator + "\n"

    # Iterate through rows
    for index, row in dataframe.iterrows():
        row_values = [
            f"\033[34m{row[column]:{width}}\033[0m"
            if index == blue_row and col_idx == blue_column
            else f"{row[column]:{width}}"
            for col_idx, (column, width) in enumerate(zip(columns, column_widths))
        ]
        df_string += " | ".join(row_values) + "\n"

    return df_string


max_lines = 13


class CSVMaster:
    def __init__(self) -> None:
        self.input_path = Path(sys.argv[1])
        read_lut = {".csv": pd.read_csv, ".xlsx": pd.read_excel, ".pkl": pd.read_pickle}
        read_fn = read_lut[self.input_path.suffix]
        self.df = read_fn(self.input_path)
        self.df_orig = self.df
        self.prompt = pyfzf.FzfPrompt()
        self.row_index = 0
        self.column_index = 0
        self.cur_value = ""

    def sort(self):
        options = list(itertools.product([True, False], self.df.columns))

        options = [{"ascending": o0, "col": o1} for o0, o1 in options]
        settings = self.prompt.prompt(options, fzf_options="--multi")
        cols = []
        ascendings = []
        for setting in settings:
            idx = [str(x) for x in options].index(setting)
            setting = options[idx]
            cols.append(setting["col"])
            ascendings.append(setting["ascending"])
        self.df = self.df.sort_values(cols, ascending=ascendings)

    def plot(self):
        potential_args = ["x", "color", "size", "facet_col", "facet_row"]
        plots = {"scatter": px.scatter, "line": px.line, "bar": px.bar}
        plottype = self.prompt.prompt(plots.keys())[0]
        plotfun = plots[plottype]
        chosen_args = ["y"] + self.prompt.prompt(potential_args, "--multi")
        arg_vals = []
        for chosen_arg in chosen_args:
            chosen_val = self.prompt.prompt(
                [f"{chosen_arg}:{x}" for x in self.df.columns if not x in arg_vals]
            )[0]
            arg_vals.append(chosen_val.replace(f"{chosen_arg}:", ""))
        print(arg_vals)

        kwargs = {k: v for k, v in zip(chosen_args, arg_vals)}
        fig = plotfun(self.df, **kwargs)
        fig.write_html("tmp.html")
        os.system("xdg-open tmp.html")

    # def filter(self):

    def exit(self):
        sys.exit()

    def less_than(self):
        column = self.prompt.prompt(self.df.columns)[0]
        value = float(input("value: "))
        self.df = self.df[self.df[column] < value]

    def more_than(self):
        column = self.prompt.prompt(self.df.columns)[0]
        value = float(input("value: "))
        self.df = self.df[self.df[column] > value]

    def str_in(self):
        column = self.prompt.prompt(self.df.columns)[0]
        value = input("string")
        self.df = self.df[self.df[column].str.contains(value)]

    def str_not_in(self):
        column = self.prompt.prompt(self.df.columns)[0]
        value = input("string")
        self.df = self.df[not self.df[column].str.contains(value)]

    # def not_str_in(self):
    def reset(self):
        self.df = self.df_orig

    def go_down(self):
        self.row_index += 1

    def go_up(self):
        self.row_index -= 1

    def go_left(self):
        self.column_index -= 1

    def go_right(self):
        self.column_index += 1

    def filter(self):
        options = [self.less_than, self.more_than, self.str_in, self.str_not_in]
        str_options = [x.__name__ for x in options]
        try:
            options[str_options.index(self.prompt.prompt(str_options)[0])]()
        except:
            print("failed")

    def write(self):
        write_lut = {
            ".csv": self.df.to_csv,
            ".xlsx": self.df.to_excel,
            ".pkl": self.df.to_pickle,
        }
        appendix = input("file appendix : ")
        new_path = self.input_path.with_stem(self.input_path.stem + f"_{appendix}")
        write_lut[new_path.suffix](new_path)

    def add_row(self):
        row = pd.DataFrame([{col: None for col in self.df.columns}])
        self.df = pd.concat([self.df, row])

    def remove_row(self):
        self.df = self.df.drop(self.row_index)

    def insert_mode(self):
        self.cur_value = self.df.iloc[self.column_index, self.row_index]
        column_type = str(self.df.iloc[:, self.column_index].dtype)
        print(column_type)
        cast_fn_lut = {"object": str, np.int64: int, np.float64: float}
        cast_fn = cast_fn_lut[column_type]

        while True:
            c = click.getchar()
            print(c)
            if c == "\r":
                break
            if c == "\x08":
                print("backspace")
                new_value = str(self.cur_value)[:-2]

            else:
                new_value = str(self.cur_value) + c
            try:
                new_value = cast_fn(new_value)
                self.cur_value = new_value
                self.df.iloc[self.row_index, self.column_index] = self.cur_value
                self.out = dataframe_to_string(
                    self.df, self.row_index, self.column_index
                )
                os.system("clear")
                print(self.out)
            except Exception as e:
                print(e)

    def __call__(self) -> Any:
        action_lut = {
            "q": self.exit,
            "s": self.sort,
            "p": self.plot,
            "j": self.go_down,
            "k": self.go_up,
            "h": self.go_left,
            "l": self.go_right,
            "f": self.filter,
            "w": self.write,
            "a": self.add_row,
            "r": self.remove_row,
            "i": self.insert_mode,
        }
        while True:
            r0 = self.row_index - max_lines // 2
            r1 = self.row_index + max_lines // 2
            r0 = min(max(r0, 0), len(self.df) - max_lines)
            r1 = min(max(r1, max_lines - 1), len(self.df) - 1)

            cur_df = self.df.iloc[r0:r1]
            self.out = dataframe_to_string(cur_df, self.row_index, self.column_index)
            os.system("clear")
            print(self.out)
            c = click.getchar()
            if c in action_lut:
                action_lut[c]()


if __name__ == "__main__":
    CSVMaster()()
