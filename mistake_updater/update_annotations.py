import numpy as np

# %%
# load Detections to change

# Load annotations  from diskstations
# for every fn mistake -> remove annotation
# for every fp mistake -> add annotation
from pathlib import Path
import pickle
import pandas as pd
from trackertoolbox.detections import Detections
from loguru import logger

from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
import pandas as pd

from utils import compute_iou

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)

scale = 8

df = pd.read_csv("test.csv")
model_directory = Path("/data/proposed")
mistake_file = list(model_directory.rglob("*_mistakes.pkl"))[1]

with open(mistake_file, "rb") as f:
    data = pickle.load(f)

mm = videosets[data["videoset"]].get_mediamanager(camera=data["camera"])
annotations = mm.load_annotations(data["annotations_suffix"])


false_neg_df = df[df.mistake_type == "false_negative"]
for c in "xywh":
    false_neg_df[f"bbox_{c}"] /= 8


# Iterate through each false negative in false_neg_df
for i, false_neg in false_neg_df.iterrows():
    annotations_t = annotations[annotations.timestamp == false_neg["timestamp"]]

    max_iou = -1  # Initialize max IoU value
    best_annotation_index = None  # Initialize the index of the best matching annotation

    # Iterate through each annotation for the current timestamp
    for index, annotation in annotations_t.iterrows():
        # Extract bounding box coordinates for false negative and annotation
        bbox_false_neg = false_neg[["bbox_x", "bbox_y", "bbox_w", "bbox_h"]].values
        bbox_annotation = annotation[["bbox_x", "bbox_y", "bbox_w", "bbox_h"]].values

        # Compute IoU between false negative and annotation
        iou = compute_iou(bbox_false_neg, bbox_annotation)

        # Update max IoU and index of best matching annotation if a better match is found
        if iou > max_iou:
            max_iou = iou
            best_annotation_index = index

    # Drop the annotation that has been picked as the best match
    if best_annotation_index is not None:
        annotations.drop(index=best_annotation_index, inplace=True)
