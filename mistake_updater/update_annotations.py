# %%
# load Detections to change

# Load annotations  from diskstations
# for every fn mistake -> remove annotation
# for every fp mistake -> add annotation
import numpy as np
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
mistake_files = list(model_directory.rglob("*_mistakes.pkl"))
mistake_files.sort()
mistake_file = mistake_files[0]

with open(mistake_file, "rb") as f:
    data = pickle.load(f)
mm = videosets[data["videoset"]].get_mediamanager(camera=data["camera"])
annotations = mm.load_annotations("smallObjectsCorrected")
if annotations is None:
    annotations = mm.load_annotations(data["annotations_suffix"])
else:
    print("loaded")

cur_len = len(annotations)
for c in "xywh":
    df[f"bbox_{c}"] /= 8
false_neg_df = df[df.mistake_type == "false_negative"]
false_pos_df = df[df.mistake_type == "false_positive"]
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
        print("dropping")
        annotations.drop(index=best_annotation_index, inplace=True)

false_pos_df = false_pos_df.drop(["confidence", "mistake_type", "eval_value", "eval_n"])
new_annotations = pd.concat([false_pos_df, annotations])

new_len = len(annotations)
logger.info(f"went from {cur_len} to {new_len} annotations")
mm.save_annotations(new_annotations, "smallObjectsCorrected")
# except:
#     continue
