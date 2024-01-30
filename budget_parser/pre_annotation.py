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
    "ov": ["ov-chipkaart"],
    "bike": ["swapfiets"],
    "insurance": ["fbto"],
    "healthcare": ["infomedics"],
    "bank": ["betaalpas"],
    "fitness": ["basic fit", "bodyfit"],
    "fun": [
        "boulder",
        "salsa",
        "mcdonalds",
        "betaalverzoek",
    ],
    "clothes": ["h&m", "zalando"],
    "phone": ["kpn"],
    "tax": ["belastingdienst"],
    "electricity": ["greenchoice"],
    "water": ["dunea"],
    "vacation": [
        "odigeo",
        "booking.com",
        "airbnb",
        "easyjet",
        "ryanair",
        "klm",
        "transavia",
        "lidl",
        "oebb",
        "wien",
        "vienna",
        "graz",
        "aut",
        "hiperdino",
        "supermercado",
    ],
    "household": ["hema", "ikea", "jysk", "action"],
    "entertainment": ["netflix", "spotify", "steam"],
    "sport": ["decathlon", "intersport"],
    "drogist": [
        "kruidvat",
    ],
    "car": ["greenwheels"],
    "loan": ["duo"],
    "internet": ["youfone"],
    "invest": ["degiro"],
}
for keyword, cats in keyword_to_cat.items():
    for i, row in df.iterrows():
        if row["Transactiebedrag"] > 0:
            continue
        for cat in cats:
            if cat in row.Omschrijving.lower():
                df.loc[i, "category"] = keyword

df.to_csv(f"{home}/2023_to_20240130_categorized.csv")

dfsorted = df.sort_values(by=["Transactiebedrag"], ascending=False)
for i, row in dfsorted.iterrows():
    if row["Transactiebedrag"] > 0:
        continue
    if row["category"] == "other":
        print(row["Omschrijving"], print(row["Transactiebedrag"]))

print(df.groupby("category")["Transactiebedrag"].sum())
