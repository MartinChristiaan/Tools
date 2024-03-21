# %%

from typing import List
import dlutils_ii as du
from annotator import BoundingBoxAnnotator
from config.dataset import get_mantis

import dlutils_ii as du

from pathlib import Path
from loguru import logger

from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)

pf = du.Pathfinder(
    "v2119_campaign1_flight02", camera="EO", quality="_hq", cache_dir="/data/sod_cache"
)

o = du.TrainOptions(
    False,
    [1],
    max_samples=120,
    annotations_suffix="ignore",  # , motion_models="compute"
)
tharde = du.DatasetConfig(pf, o)
annotator = BoundingBoxAnnotator(tharde).run()
