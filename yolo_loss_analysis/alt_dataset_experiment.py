# %%
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

import scienceplots

plt.style.use("science")
data = "/mnt/toren/data/leeuwenmcv/general/alt_dataset_experiment"
data2 = f"/mnt/dl-3/data/leeuwenmcv/general/tyolo"

results2 = list(Path(data2).glob("*/results.csv"))
proposed = [x for x in results2 if "proposed" == x.parent.name]

print(proposed)

# %%


results = list(Path(data).glob("*/results.csv")) + proposed
results.sort()

names = []
for result in results:
    names += [result.parent.name]
# idxs =  prompt(names,multi=True,return_idx=True)
idxs = range(len(names))
# results_to_show = [results[idx] for idx in idxs]
dfs = []
best_data = []
for idx in idxs:
    result = results[idx]
    name = names[idx]
    df = pd.read_csv(result)
    best_idx_col = "    metrics/mAP50-95(B)"
    best_idx = df[best_idx_col].argmax()
    for col in df.columns:
        if not "metric" in col:
            continue
        best_data.append(dict(model=name, metric=col, value=list(df[col])[best_idx]))
    #
df = pd.DataFrame(best_data)

metrics = df.metric.unique()
metrics_to_keep = [
    x for x in metrics if "precision" in x or "mAP50(" in x or "recall" in x
]
name_lut = dict(zip(metrics_to_keep, ["precision", "recal", "mAP50"]))
df = df[df.metric.isin(metrics_to_keep)]
df["metric"] = [name_lut[x] for x in df.metric]

# # Plotting with matplotlib

# curnames = [
#     "combined_tyolo8m_balanced_02022024",
#     "combined_tyolo8m_cropped_02022024",
#     "combined_tyolo8m_regular_02022024",
#     "combined_yolo8m_balanced_02022024",
#     "combined_tyolo8m_no_bbox_clip_02022024",
# ]
curnames = list(df.model.unique())
print(curnames)

newnames = [
    "proposed",
    "virat mixed",
    "virat only",
    "visdrone mixed",
    "visdrone only",
]
name_lut = dict(zip(curnames, newnames))
df = df[df.model.isin(curnames)]
df["model"] = [name_lut[x] for x in df.model]
# print(df)
models = df["model"].unique()  # Get unique model names
metrics = df["metric"].unique()  # Get unique metrics names

df.to_csv("overview_results_re.csv", index=False)

# Plot bars for each metric for each model
bar_width = 0.8  # Width of each bar
# models = df.model.unique()
maps = list(df[df["metric"] == "mAP50"]["value"])
# models = df[df["metric"] == "mAP50"]["model"]
# %%
map_sort = np.argsort(maps)[::-1]
print(map_sort)

fig, ax = plt.subplots(figsize=(3, 3))  # Set the size of the figure

colors = plt.cm.tab20.colors  # Get a list of colors for each metric
for i, metric in enumerate(metrics[-1:]):
    x = np.arange(len(models))  # [map_sort]
    y = np.array(df[df["metric"] == metric]["value"])[map_sort]  # Y-axis values
    ax.bar(x, y, width=bar_width, label=metric, color=colors[i])

ax.set_xticks(range(len(models)))  # Set ticks on X-axis
ax.set_xticklabels(
    models[map_sort], rotation=45, ha="right"
)  # Set labels on X-axis with rotation
ax.set_ylabel("mAP")  # Set label for Y-axis
ax.set_xlabel("Model")  # Set label for X-axis
# ax.legend()  # Add legend
plt.grid(1)
plt.tight_layout()  # Ensure tight layout
plt.savefig("exp_external_datasets.pdf", dpi=300)  # Save plot in vector format (PDF)
plt.savefig(
    "exp_external_datasets.png", dpi=300, transparent=True
)  # Save plot in vector format (PDF)
plt.show()  # Show plot

# %%


# fig = px.bar(df, barmode="group", x="model", y="value", color="metric")
# fig.show()

# %%
