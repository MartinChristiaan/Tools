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


def rotterdam_harbour(output_dir):
    configs = []
    pathfinder = du.Pathfinder(
        videoset="rotterdam_harbour_20210308", camera="jai20000", cache_dir=output_dir
    )
    train_options = du.TrainOptions(
        val=True,
        offset_scales=[3],
        max_samples=100,
        annotations_suffix="panoptes_exp",
        crop=[633, 1058, 1656, 974],
    )
    config = du.DatasetConfig(pathfinder, train_options)
    configs.append(config)
    return configs


datasets = rotterdam_harbour("/data/sod_cache")
du.Writer(datasets[0], [0, -15, 15]).write()
BoundingBoxAnnotator(datasets[0]).run()
