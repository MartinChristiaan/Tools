from pathlib import Path

import pandas as pd

from SFzfPrompt import prompt

# train_dir = f"/mnt/dl-41/data/leeuwenmcv/mantis/tyolov8-cv90"
# train_dir = f"/mnt/dl-41/data/leeuwenmcv/mantis/mantis-tyolov8"
# train_dir = f"/mnt/dl-41/data/leeuwenmcv/general/ratio/yolo"
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
results_to_use = prompt(results, True, "results_to_plot")

for x in results_to_use:
    modelname = x.parent
    df = pd.read_csv(x)
    df["model"] = len(df) * [modelname]


# model_names =
