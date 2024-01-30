# %%
import pandas as pd
import os

home = os.path.expanduser("~")
df = pd.read_excel(f"{home}/2023_to_20240130.xls")
df["category"] = ["fun"] * len(df)
description = df["Omschrijving"]
df = df[df["Transactiebedrag"] < 0]

keyword_to_cat = {
    "rent": ["vastgoed"],
    "groceries": ["hoogvliet", "jumbo", "albert", "heijn", "samara"],
    "misc": ["bol.com"],
    "ov": ["ov-chipkaart", "ns-", "ret"],
    "bike": ["swapfiets"],
    "insurance": ["fbto"],
    "healthcare": ["infomedics"],
    "bank": ["betaalpas", "abn amro"],
    "fitness": ["basic fit", "body fit", "leiden", "basicfit"],
    "fun": ["boulder", "salsa", "mcdonalds", "tikkie", "eversport", "tno", "musicon"],
    "clothes": ["h&m", "zalando"],
    "phone": ["kpn"],
    "tax": ["belastingdienst", "gemeente", "belasting"],
    "electricity": ["greenchoice"],
    "water": ["dunea"],
    "vacation": [
        "grc",
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
        "international card services",
        "betaalverzoek",
        "wiebetaaltwat",
        "int card services",
    ],
    "household": ["hema", "ikea", "jysk", "action"],
    "entertainment": ["netflix", "spotify", "steam"],
    "sport": ["decathlon", "intersport"],
    "drogist": [
        "kruidvat",
    ],
    "car": ["greenwheels"],
    "loan": ["duo", "dienst uitvoering onderwijs"],
    "internet": ["youfone"],
    "invest": ["degiro", "flatex"],
    "haircut": ["hizi hair"],
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
