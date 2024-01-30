# %%
import pandas as pd
import os

home = os.path.expanduser("~")
df = pd.read_excel(f"{home}/2023_to_20240130.xls")
df["category"] = ["other"] * len(df)
description = df["Omschrijving"]
df = df[df["Transactiebedrag"] < 0]

keyword_to_cat = {
    "rent": ["vastgoed"],
    "groceries": ["hoogvliet", "jumbo", "albert", "heijn"],
    "misc": ["bol.com"],
    "vacation": ["wien", "vienna", "graz"],
    "ov": ["ov-chipkaart"],
    "bike": ["swapfiets"],
    "insurance": ["fbto"],
    "healthcare": ["infomedics"],
    "fun": ["boulder"],
    "clothes": ["h&m", "zalando"],
    "phone": ["kpn"],
    "tax": ["belastingdienst"],
}

for keyword, cats in keyword_to_cat.items():
    for i, row in df.iterrows():
        if row["Transactiebedrag"] > 0:
            continue
        for cat in cats:
            if cat in row.Omschrijving.lower():
                df.loc[i, "category"] = keyword

df.to_csv(f"{home}/2023_to_20240130_categorized.csv")

print(df.groupby("category")["Transactiebedrag"].sum())
