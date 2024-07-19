from pathlib import Path

import pandas as pd

from utils.SFzfPrompt import prompt

# train_dir = f"/mnt/dl-41/data/leeuwenmcv/mantis/tyolov8-cv90"
# train_dir = f"/mnt/dl-41/data/leeuwenmcv/mantis/mantis-tyolov8"
# train_dir = f"/mnt/dl-41/data/leeuwenmcv/general/ratio/yolo"
train_dir = prompt(
    [
        f"/mnt/dl-41/data/leeuwenmcv/general/l3harris",
        f"/mnt/dl-41/data/leeuwenmcv/general/tyolo",
        f"/mnt/dl-3/data/leeuwenmcv/general/tyolo",
        f"/mnt/dl-3/data/leeuwenmcv/general/ratio/yolo",
        f"/mnt/dl-41/data/leeuwenmcv/general/p2-experiment",
        f"/mnt/toren/data/leeuwenmcv/general/p2-experiment",
        f"/mnt/toren/data/leeuwenmcv/general/alt_dataset_experiment/",
    ]
)


results = list(Path(train_dir).glob("*/results.csv"))
results.sort()
names = []
for result in results:
    names += [result.parent.name]
# idxs =  prompt(names,multi=True,return_idx=True)
idxs = range(len(names))
# results_to_show = [results[idx] for idx in idxs]
dfs = []
for idx in idxs:
    result = results[idx]
    name = names[idx]
    df = pd.read_csv(result)
    df.columns = [col.strip() for col in df.columns]
    metric_names = [col for col in df.columns if "metric" in col or "loss" in col]
    melted_df = pd.melt(
        df,
        id_vars=["epoch"],
        value_vars=metric_names,
        var_name="metric",
        value_name="score",
    )
    melted_df["name"] = [name] * len(melted_df)
    dfs += [melted_df]

df = pd.concat(dfs)
import plotly.express as px

# Create a faceted line plot
fig = px.line(
    df,
    x="epoch",
    y="score",
    color="name",
    facet_row="metric",
    labels={"score": "Score", "epoch": "Epoch"},
    title="Metrics Over Epochs by Metric",
    height=2000,
)
fig.update_yaxes(matches=None)
fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
# Customize the layout
# fig.update_layout(
#     xaxis_title='Epoch',
#     yaxis_title='Score',
#     showlegend=True,
#     legend_title='Name',
# )

# Show the plot
fig.show()


# print(df.columns)


# print(result)
