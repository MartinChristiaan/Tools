# %%
# parse excel
import datetime
import os

import pandas as pd

home = os.path.expanduser("~")
df = pd.read_excel(f"{home}/budget_2024.xls")
# %%
descriptions = df["description"].unique()

from dataclasses import dataclass


@dataclass
class Statement:
    description: str
    amount: float
    date: datetime.datetime

    @staticmethod
    def from_df(df):
        return [Statement(**row) for i, row in df.iterrows()]


@dataclass
class BudgetCategory:
    name: str
    monthly: int
    keywords: list[str]
    statements: list[str] = None


budget_categories = [
    BudgetCategory("groceries", 400, ["jumbo", "hoogvliet", "albert", "samara"]),
]


# def assign_category(description):
#     current_cat = "other"
#     for category in budget_categories:
#         for keyword in category.keywords:
#             if keyword in description:
#                 if current_cat != "other":
#                     raise ValueError(
#                         f"Multiple categories found for description {description}"
#                     )
#                 current_cat = category.name
#     return current_cat


# for i, row in df.iterrows():
#     df.loc[i, "category"] = assign_category(row["description"])
