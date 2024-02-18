from pathlib import Path

import pandas as pd

from SFzfPrompt import prompt
from charmenu import charmenu
from click import getchar

# train_dir = f"/mnt/dl-41/data/leeuwenmcv/mantis/tyolov8-cv90"
# train_dir = f"/mnt/dl-41/data/leeuwenmcv/mantis/mantis-tyolov8"
# train_dir = f"/mnt/dl-41/data/leeuwenmcv/general/ratio/yolo"
print("use latest data? \n")
use_latest_data = getchar() == "y"
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

# for every sequencename generate a barplot with the recall and precision per model
import matplotlib.pyplot as plt

# Group the data by sequencename and model
grouped_data = latest_data_df.groupby(["name", "model"]).mean().reset_index()

# Iterate over each sequencename
for sequencename in grouped_data["name"].unique():
    # Filter the data for the current sequencename
    sequencename_data = grouped_data[grouped_data["name"] == sequencename]

    # Create a bar plot for recall and precision
    plt.figure()
    plt.bar(sequencename_data["model"], sequencename_data["F1 Recall"], label="Recall")
    # plt.bar(
    #     sequencename_data["model"], sequencename_data["F1 Precision"], label="Precision"
    # )
    plt.xlabel("Model")
    plt.ylabel("Score")
    plt.title(f"Recall and Precision for {sequencename}")
    plt.legend()
    plt.savefig(f"{sequencename}_barplot.png")
