# %%
import pandas as pd

df = pd.read_excel("2023.xls")

df["maand"] = df["Transactiedatum"].apply(lambda x: int(str(x)[4:6]))
# df.Omschrijving=


class BudgetDF(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super(BudgetDF, self).__init__(*args, **kwargs)

    @property
    def Rekeningnummer(self):
        return "Rekeningnummer"

    @property
    def Muntsoort(self):
        return "Muntsoort"

    @property
    def Transactiedatum(self):
        return "Transactiedatum"

    @property
    def Rentedatum(self):
        return "Rentedatum"

    @property
    def Beginsaldo(self):
        return "Beginsaldo"

    @property
    def Eindsaldo(self):
        return "Eindsaldo"

    @property
    def Transactiebedrag(self):
        return "Transactiebedrag"

    @property
    def Omschrijving(self):
        return "Omschrijving"


boodschappen = ["jumbo", "hoogvliet", "albert"]


# df_boodschappen.Transactiebedrag
# df_boodschappen.plot.bar('Transactiedatum',)


# print(df_b)
