import argparse
from dataclasses import dataclass
import os
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from utils.dataframe_utils import load_config


@dataclass
class BudgetCat:
    name: str
    cat: int

    @staticmethod
    def from_df(df):
        return [BudgetCat(**row) for i, row in df.iterrows()]


def calc_per_maand(df, str_contained, cat):
    contained_rows = []
    for i, row in df.iterrows():
        if row["Transactiebedrag"] > 0:
            continue
        for b in str_contained:
            if b in row.Omschrijving.lower():
                contained_rows.append(i)
                continue
    df_contained = df.iloc[contained_rows]
    print(df_contained)

    maandsom = df_contained.groupby("maand")["Transactiebedrag"].sum()
    print(f"{cat} avg : {maandsom.sum()/8}")
    maanden = df_contained["maand"].unique()
    import matplotlib.pyplot as plt

    months_list = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    months_list = [months_list[x - 1] for x in maanden]

    plt.figure(figsize=(16, 9))
    plt.bar(months_list, -maandsom)
    plotsdir = Path("plots")
    plotsdir.mkdir(exist_ok=True)
    plt.savefig(plotsdir / f"{cat}.png")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ExampleProgram", description="ExampleDescription"
    )
    parser.add_argument("-c", "--config", type=str, default="config/default.csv")
    parser.add_argument("-q", "--query", type=str, default="config/query_all.py")
    args = parser.parse_args()
    updated_df = load_config(BudgetCat, args.config, args.query)
    budgetcat = BudgetCat.from_df(updated_df)
    cats = np.unique([x.cat for x in budgetcat])
    home = os.path.expanduser("~")
    df = pd.read_excel(f"{home}/budget_2024.xls")
    df["maand"] = df["Transactiedatum"].apply(lambda x: int(str(x)[4:6]))
    for cat in cats:
        str_contained = [x.name for x in budgetcat if x.cat == cat]
        print(str_contained, cat)
        calc_per_maand(df, str_contained, cat)

    # resterende_uitgaven = df[df.Transactiebedrag<0].sum()/8
    # print(f"all_avg : {resterende_uitgaven}" )
    # for person in tqdm(persons):

    # for c in budgetcat:
    # contained_rows=action(budgetcat,df)

    # lut = {}
