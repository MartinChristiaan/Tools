# %%
from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd

import scienceplots

plt.style.use("science")
data = "/mnt/toren/data/leeuwenmcv/general/p2-experiment"
csv_files = list(Path(data).glob("*/results.csv"))

names = [x.parent.stem for x in csv_files]
models = [x.split("_")[0] for x in names]
bbox_sizes = [int(x.split("_")[-1]) for x in names]

# %%


recalls = []
for csv_file in csv_files:
    print(csv_file)
    df = pd.read_csv(csv_file)
    print(df.columns)
    recall = df["      metrics/recall(B)"].max()
    recalls.append(recall)

print(models, bbox_sizes, recalls)

df = pd.DataFrame({"model": models, "bbox_size": bbox_sizes, "recall": recalls})

plt.figure(figsize=(10, 5))
for model, model_df in df.groupby("model"):
    model_df = model_df.sort_values("bbox_size")
    plt.plot(model_df["bbox_size"], model_df["recall"], "-o", label=model)
plt.legend()
plt.xlabel("Min bbox size")
plt.ylabel("Recall")
plt.grid(1)
plt.savefig("p2_experiment.png")
plt.savefig("p2_experiment.pdf")

plt.show()

# %%
