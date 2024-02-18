# %%
from pathlib import Path

import pandas as pd

from SFzfPrompt import prompt
from charmenu import charmenu
from click import getchar

# train_dir = f"/mnt/dl-41/data/leeuwenmcv/mantis/tyolov8-cv90"
# train_dir = f"/mnt/dl-41/data/leeuwenmcv/mantis/mantis-tyolov8"
# train_dir = f"/mnt/dl-41/data/leeuwenmcv/general/ratio/yolo"
print("use latest data? \n")
# use_latest_data = getchar() == "y"
use_latest_data = True  # @ getchar() == "y"
if not use_latest_data:
    train_dir = prompt(
        [
            f"/mnt/dl-41/data/leeuwenmcv/general/tyolo",
            f"/mnt/dl-3/data/leeuwenmcv/general/tyolo",
            f"/mnt/dl-41/data/leeuwenmcv/general/p2-experiment",
            f"/mnt/toren/data/leeuwenmcv/general/p2-experiment",
        ]
    )

    results = list(Path(train_dir).glob("*/metrics_per_config.csv"))
    results.sort()
    print("use all data? \n")
    use_all = getchar() == "y"
    if use_all:
        results_to_use = results
    else:
        results_to_use = prompt(results, True, "results_to_plot")
    df_list = []
    for x in results_to_use:
        x = Path(x)
        modelname = x.parent
        df = pd.read_csv(x)
        df["model"] = len(df) * [modelname]
        df_list.append(df)

    latest_data_df = pd.concat(df_list)
    latest_data_df.to_csv("latest_data.csv", index=False)
else:
    latest_data_df = pd.read_csv("latest_data.csv")

print(latest_data_df.columns)
# Index(['Unnamed: 0.1', 'Unnamed: 0', 'name', 'F1', 'F1 Precision', 'F1 Recall',
#        'F1 Threshold', 'F1 FPPI', 'mAP', 'bbox_size_median', 'bbox_size_std',
#        'bbox_size_min', 'bbox_size_max', 'num_frames', 'model'],
#       dtype='object')
sequences = latest_data_df["name"].unique()


air_sequences = [x for x in sequences if "mantis_drone_2023" in x]
naval_sequences = [x for x in sequences if "rotterdam" in x]
ground_sequences = [x for x in sequences if not x in air_sequences + naval_sequences]

import matplotlib.pyplot as plt

# Define the models and categories
models = latest_data_df["model"].unique()
categories = ["air", "naval", "ground"]

# Initialize lists to store the mean mAP values
air_means = []
naval_means = []
ground_means = []

# Calculate the mean mAP values for each model and category
for modelname in models:
    air_mean = latest_data_df[
        latest_data_df["name"].isin(air_sequences)
        & (latest_data_df["model"] == modelname)
    ].mAP.mean()
    naval_mean = latest_data_df[
        latest_data_df["name"].isin(naval_sequences)
        & (latest_data_df["model"] == modelname)
    ].mAP.mean()
    ground_mean = latest_data_df[
        latest_data_df["name"].isin(ground_sequences)
        & (latest_data_df["model"] == modelname)
    ].mAP.mean()

    air_means.append(air_mean)
    naval_means.append(naval_mean)
    ground_means.append(ground_mean)

# Set the width of the bars
bar_width = 0.25

# Set the positions of the bars on the x-axis
r1 = range(len(models))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Create the bar chart
plt.bar(r1, air_means, width=bar_width, label="Air")
plt.bar(r2, naval_means, width=bar_width, label="Naval")
plt.bar(r3, ground_means, width=bar_width, label="Ground")

# Add labels, title, and legend
plt.xlabel("Model")
plt.ylabel("mAP")
plt.title("Mean mAP per Model and Category")
plt.xticks([r + bar_width for r in range(len(models))], models)
plt.legend()

# Show the bar chart
plt.show()


# # for every sequencename generate a barplot with the recall and precision per model
# import matplotlib.pyplot as plt

# # Group the data by sequencename and model

# import plotly.express as px

# # sequencename_data = grouped_data[grouped_data["name"] == sequencename]

# # Create a bar plot for recall and precision
# fig = px.bar(
#     latest_data_df,
#     x="model",
#     y="mAP",
#     # labels={"model": "Model", "F1 mAP": "mAP"},
#     color="name",
#     # title=f"Recall for {sequencename}",
# )
# fig.show()

# # %%

# %%
