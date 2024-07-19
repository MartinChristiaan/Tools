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
vset = videosets["visdrone_2019"]
mm = vset.get_mediamanager("uav0000086_00000_v")
print(mm.load_annotations())
