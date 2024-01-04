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
# %%
for cam in vset.cameras:
    new_annot = None
    for x in new_annotations:
        if cam.replace("/", "_") in x:
            new_annot = x
    if new_annot is None:
        continue
    print(new_annot)

    mm = vset.get_mediamanager(cam)
    annotations = mm.load_annotations("smallObjectsCorrected")
    if annotations is None:
        annotations = mm.load_annotations("static")
