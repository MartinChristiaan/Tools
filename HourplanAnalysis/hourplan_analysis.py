
# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


ourplan = pd.read_csv("./ourplan_new.csv")
print(ourplan.columns)


plan_columns = [c for c in ourplan.columns if c.startswith(
    "Plan") and "2022" in c]
real_columns = [c for c in ourplan.columns if c.startswith(
    "Real") and "2022" in c]

for i, row in ourplan.iterrows():
    total_planned = sum(row[c] for c in plan_columns)
    total_real = sum(row[c] for c in real_columns)
    if total_planned + total_real > 0:
        if str(row["WBS name"]) != "nan":
            print(
                f'{row["Project name"]} {row["WBS name"]}: {total_real}/{total_planned}')


plan_columns = [c for c in ourplan.columns if c.startswith("Plan ")]
real_columns = [c for c in ourplan.columns if c.startswith("Real ")]

os.makedirs('project_plots', exist_ok=True)

for i, row in tqdm(list(ourplan.iterrows())):
    total_planned = sum(row[c] for c in plan_columns)
    total_real = sum(row[c] for c in real_columns)
    if total_planned + total_real > 0:
        if str(row["WBS name"]) == "nan":
            planned = np.cumsum([row[c] for c in plan_columns])

            real = np.cumsum([row[c] for c in real_columns])
            labels = [c.split(" ")[2].replace("*","") for c in plan_columns]
            plt.figure(figsize=(25, 9))
            plt.plot(real)
            plt.plot(planned,"--")
            plt.xticks(np.arange(len(labels)), labels)
            plt.title(f"Hours {row['Project name']}")
            plt.xlabel("Week")
            plt.ylabel("Hours")
            plt.grid(1)
            plt.legend(['real', 'planned'])
            plt.savefig(
                f'project_plots/{row["Project name"]}.png')
