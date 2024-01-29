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
    BudgetCategory("other", 0, [], []),
]


def assign_category(statement: Statement, budget_categories: list[BudgetCategory]):
    category = None
    for cat in budget_categories:
        for keyword in cat.keywords:
            if keyword in statement.description.lower():
                if not category is None:
                    raise Exception(
                        f"{statement.description} is in multiple categories"
                    )
                cat.statements.append(statement)
                category = cat
                break
    if category is None:
        budget_categories[-1].statements.append(statement)


for statement in statements:
    assign_category(statement, budget_categories)

for cat in budget_categories:
    print(cat)

# %%
