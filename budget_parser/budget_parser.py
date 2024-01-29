# %%
# parse excel
import datetime
import os
import re

import pandas as pd
from matplotlib import category

home = os.path.expanduser("~")
df = pd.read_excel(f"{home}/budget_2024.xls")
# %%
descriptions = df["description"].unique()

from dataclasses import dataclass


def clean_description(description: str):
    "remove double spaces and make lowercase and remove non word characters except spaces"
    # description = description.lower()
    description = description.lower().replace("  ", " ")
    description = re.sub(r"[^\w\s]", "", description)
    return description


@dataclass
class Statement:
    description: str
    amount: float
    date: datetime.datetime

    @staticmethod
    def from_dict(dict):
        date = dict["transactiondate"]
        # parse 20231229 to datetime
        date = datetime.datetime.strptime(str(date), "%Y%m%d")
        return Statement(row["description"], row["amount"], date)

    def __repr__(self) -> str:
        return f"{clean_description(self.description)} : {self.amount} : {self.date}"


statements = []
for i, row in df.iterrows():
    statements.append(Statement.from_dict(row))
print(statements)


# %%


@dataclass
class BudgetCategory:
    name: str
    monthly: int
    keywords: list[str]
    statements: list[Statement]

    def __repr__(self) -> str:
        statements = "\n".join([str(x) for x in self.statements])
        return f"{self.name} : {self.monthly} \n {statements}"


budget_categories = [
    BudgetCategory("groceries", 400, ["jumbo", "hoogvliet", "albert", "samara"], []),
    BudgetCategory("rent", 800, ["vastgoed"], []),
    BudgetCategory("health", 800, [], []),
    BudgetCategory("bike", 800, ["swapfiets"], []),
    BudgetCategory("gym", 800, ["basic-fit"], []),
    BudgetCategory("health", 800, ["med"], []),
    BudgetCategory("gifts", 800, [], []),
    BudgetCategory("clothing", 800, [], []),
    BudgetCategory("internet", 800, [], []),
    BudgetCategory("guy activities", 800, [], []),
    BudgetCategory("haircut", 800, [], []),
    BudgetCategory("other", 0, [], []),
]
