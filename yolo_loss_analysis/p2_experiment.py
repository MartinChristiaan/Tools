# %%
from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd

data = "/mnt/toren/data/leeuwenmcv/general/p2-experiment"
csv_files = Path(data).glob("*/results.csv")

names = [x.parent.stem for x in csv_files]
models = [x.split("_")[0] for x in names]
bbox_sizes = [int(x.split("_")[-1]) for x in names]

# %%

recalls = []
for csv_file in csv_files:
    print(csv_file)
    df = pd.read_csv(csv_file)
    recall = df["recall"].max()
    recalls.append(recall)

print(models, bbox_sizes, recalls)

df = pd.DataFrame({"model": models, "bbox_size": bbox_sizes, "recall": recalls})

plt.figure()
for model, model_df in df.groupby("model"):
    plt.plot(model_df["bbox_size"], model_df["recall"], label=model)
plt.legend()
plt.xlabel("bbox size")
plt.ylabel("recall")
plt.show()
