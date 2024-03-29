# %%
import scienceplots
from hmac import new
from pathlib import Path

import pandas as pd

from SFzfPrompt import prompt
from charmenu import charmenu
import matplotlib.pyplot as plt
from click import getchar
import pandas as pd

# plt.style.use("ggplot")
plt.style.use("science")

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
new_models = []
for model in latest_data_df["model"]:
    if "air_to_ground" in model:
        new_models.append("air_to_ground")
    elif "naval" in model:
        new_models.append("naval")
    elif "ground" in model:
        new_models.append("ground")
    else:
        new_models.append("generic")
latest_data_df["model"] = new_models


air_sequences = [x for x in sequences if "mantis_drone_2023" in x]
naval_sequences = [x for x in sequences if "rotterdam" in x]
ground_sequences = [x for x in sequences if not x in air_sequences + naval_sequences]


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

    air_means.append(int(air_mean * 100))
    naval_means.append(int(naval_mean * 100))
    ground_means.append(int(ground_mean * 100))

# Create a dataframe to store the mean mAP values
mean_mAP_df = pd.DataFrame(
    {
        "Model": models,
        "Air Mean mAP (%)": air_means,
        "Naval Mean mAP (%)": naval_means,
        "Ground Mean mAP (%)": ground_means,
    }
)

# Save the dataframe as a CSV file
mean_mAP_df.to_csv("mean_mAP_results.csv", index=False)

# Set the width of the bars
bar_width = 0.25

# Set the positions of the bars on the x-axis
r1 = range(len(models))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(r1, air_means, width=bar_width, label="Air data")
plt.bar(r2, naval_means, width=bar_width, label="Naval data")
plt.bar(r3, ground_means, width=bar_width, label="Ground data")

# Add labels, title, and legend
plt.xlabel("Model")
plt.ylabel("mAP")
plt.title("mAP per Model and Dataset")
plt.xticks([r + bar_width for r in range(len(models))], models)
plt.legend()
plt.grid(1)
# Show the bar chart

plt.savefig("mAP_per_model_and_dataset.pdf")


# %%
