# %%
import os
from pathlib import Path

import pandas as pd
from loguru import logger
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
from videosets_ii.videosets_ii import VideosetsII

videosets = VideosetsII(None)  # basedirpath)
cameras = [x for x in videosets["mantis_drone_2023"].cameras if x.endswith("wide_hd")]
vset = videosets["mantis_drone_2023"]
newpath = Path(f"\\\\diskstationii1/{vset.relative_path}")
# print(newpath.exists())
# print(newpath)
# items = list(newpath.rglob("*"))
os.system("rsync -azP /")
