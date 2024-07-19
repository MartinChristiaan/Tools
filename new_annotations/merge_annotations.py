# %%
import os
from pathlib import Path
from loguru import logger

from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)

vset = videosets["mantis_drone_2023"]
new_annotations = [str(x) for x in Path(".").glob("*.csv")]
print(new_annotations)
for cam in vset.cameras:
    new_annot = None
    for x in new_annotations:
        if cam.replace("/", "_") in x:
            new_annot = x
    if new_annot is None:
        continue

    mm = vset.get_mediamanager(cam)
    annotations_old = mm.load_annotations("smallObjectsCorrected")
    if annotations_old is None:
        annotations_old = mm.load_annotations("static")
    annotations_new = pd.read_csv(new_annot)
    annotations_new = annotations_new[annotations_new.label != "ignore_frame"]
    if not annotations_old is None:
        t_new = annotations_new.timestamp
        t_old = [x for x in annotations_old.timestamp if not x in t_new]
        annotations_new = pd.concat(
            [annotations_new, annotations_old[annotations_old.timestamp.isin(t_old)]]
        )
        logger.info(
            f"updated annotations, old len {len(annotations_old)}, new len {len(annotations_new)} {cam}"
        )
    else:
        logger.info(f"{len(annotations_new)} new annotations for {cam}")
    if len(annotations_new) > 0:
        mm.save_annotations(annotations_new, "smallObjectsCorrected", True)
