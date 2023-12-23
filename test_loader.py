# %%
import pandas as pd

df = pd.read_csv("spear.csv")
print(df)
# %%

df = df.set_index("log_column")
# %%
print(df.index)
df["log_column"] = df.index
print(df.to_dict("records"))
