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
    "bol.com": ["bol.com"],
    "ov": ["ov-chipkaart", "ns-", "ret"],
    "bike": ["swapfiets", "thijs brand"],
    "insurance": ["fbto"],
    "healthcare": ["infomedics"],
    "bank": ["abn amro"],
    "fitness": ["basic fit", "body fit", "leiden", "basicfit"],
    "fun": [
        "boulder",
        "salsa",
        "mcdonalds",
        "tikkie",
        "eversport",
        "tno",
        "musicon",
        "betaalverzoek",
    ],
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
        "wiebetaaltwat",
        "int card services",
        "land:",
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
# %%
dfsorted = df.sort_values(by=["Transactiebedrag"], ascending=False)
for i, row in dfsorted.iterrows():
    if row["Transactiebedrag"] > 0:
        continue
    if row["category"] == "other":
        print(row["Omschrijving"], print(row["Transactiebedrag"]))

print(df.groupby("category")["Transactiebedrag"].sum())

# category = input("Enter a category: ")

# dfsorted = df[df["category"] == category].sort_values(
#     by=["Transactiebedrag"], ascending=False
# )
# for i, row in dfsorted.iterrows():
#     if row["Transactiebedrag"] > 0:
#         continue
#     if row["category"] == category:
#         print(row["Omschrijving"], print(row["Transactiebedrag"]))
import plotly.graph_objects as go

df["date"] = pd.to_datetime(df["Transactiedatum"], format="%Y%m%d")
expense_per_category_per_month = df.groupby(
    [pd.Grouper(key="date", freq="M"), "category"]
)["Transactiebedrag"].sum()

# Reindex to include all categories and months
categories = df["category"].unique()
months = pd.date_range(start=df["date"].min(), end=df["date"].max(), freq="M")
expense_per_category_per_month = expense_per_category_per_month.reindex(
    pd.MultiIndex.from_product([months, categories], names=["date", "category"]),
    fill_value=0
)

categories = df["category"].unique()

for category in categories:
    category_data = expense_per_category_per_month.loc[:, category]
    fig = go.Figure(
        data=[
            go.Bar(
                x=category_data.index.get_level_values("date"), y=category_data.values
            )
        ]
    )
    fig.add_trace(
        go.Scatter(
            x=category_data.index.get_level_values("date"),
            y=[category_data.mean()] * len(category_data),
            mode="lines",
            name="Average",
        )
    )
    fig.update_layout(title=category)
    fig.show()

# print(expense_per_category_per_month)

# %%
