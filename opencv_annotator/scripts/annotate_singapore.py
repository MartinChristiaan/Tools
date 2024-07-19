# %%
%load_ext autoreload
%autoreload 2


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

def wereld_havendagen(output_dir):
    pathfinder = du.Pathfinder(
        videoset="wereldhavendagen_2016_HR", camera="opname5", cache_dir=output_dir
    )
    train_options = du.TrainOptions(
        val=False,
        offset_scales=[2.5],
        max_samples=30,
        # blur=1,
        # scale=1,
        # scale_var=0.2,
    )
    config = du.DatasetConfig(pathfinder, train_options)
    return [config]


def singapore(output_dir) -> List[du.DatasetConfig]:
    vset = videosets["singapore"]
    configs = []
    for camera in vset.cameras:
        pathfinder = du.Pathfinder(
            videoset="singapore", camera=camera, cache_dir=output_dir
        )
        train_options = du.TrainOptions(
            val=False,
            offset_scales=[3],
            max_samples=10,
        )
        config = du.DatasetConfig(pathfinder, train_options)
        configs.append(config)
    return configs


def ijmuiden(output_dir):
    vset = videosets["IJmuiden_2018"]
    configs = []
    for camera in vset.cameras:
        if not "vis" in camera.lower():
            continue
        pathfinder = du.Pathfinder(
            videoset="IJmuiden_2018", camera=camera, cache_dir=output_dir
        )
        train_options = du.TrainOptions(
            val=False,
            offset_scales=[1],
            max_samples=10,
        )
        config = du.DatasetConfig(pathfinder, train_options)
        configs.append(config)
    return configs


def tno_tower(output_dir):
    vset = videosets["tno_tower_20230426"]
    configs = []
    for camera in vset.cameras:
        pathfinder = du.Pathfinder(
            videoset="tno_tower_20230426", camera=camera, cache_dir=output_dir
        )
        train_options = du.TrainOptions(
            val=False,
            offset_scales=[1],
            max_samples=10,
        )
        config = du.DatasetConfig(pathfinder, train_options)
        configs.append(config)
    return configs



datasets = singapore('/data/sod_cache')
# BoundingBoxAnnotator(datasets[35]).run()
for x in datasets:
    # annotator = BoundingBoxAnnotator(x)
    tmp_path = x.pathfinder.annotations_path.with_suffix('.tmp.csv')
    annotations = pd.read_csv(tmp_path)
    x.pathfinder.media_manager.save_annotations(annotations,'smallObjectsCorrected',True)
    logger.info(f'saved {tmp_path}')
