from pathlib import Path
from typing import List

import dlutils_ii as du
import numpy as np
import pandas as pd
from loguru import logger
from videosets_ii.videosets_ii import VideosetsII


# # Dataset Configuration
# Configuration is done using python code. Initially I used yaml files but i found that it was often a lot of work to configure experiments this way. By leveraging the scripting capabilities of python, the configuration can be done without too much effort.
# Typically configuration is saved to a script in the config directory so that it can be used acros multiple scripts.
# Note that a lot of parameters need to be set per videoset, as dataset characteristics such as resolution, object size and object speeds can be rather diverse.
# %%
def get_example_dataset_configs(
    diskstation_dir="/diskstation", cache_dir="/data/example_dataset"
) -> List[du.DatasetConfig]:
    basedirpath = Path(
        diskstation_dir
    )  # Where to videosets can be found, use smbmount on this location to load various datasources
    videosets = VideosetsII(basedirpath=basedirpath)

    singapore = videosets["singapore"]
    # you can use this helper function to limit your selection to annotated cameras
    annotated_singapore = du.get_cameras_with_annotations(singapore)
    annotated_singapore.sort()

    configs = []
    for c in annotated_singapore[:5]:
        # for demo, purposes we only use three cameras for training
        pathfinder = du.Pathfinder(
            videoset="singapore",
            camera=c,
            cache_dir=cache_dir,  # where the training data should be exported locally
        )
        train_options = du.TrainOptions(
            val=False,
            # Every yolo variant will have a frame-offset to sample nearby frames.
            # We want the model to recognize objects at various speed, so typically, we want to sample multiple offset scales.
            offset_scales=[1, 2],
            # Datasets may have a lot of annotated frames but may have limited variety, with the max samples variable you
            # can control how many samples are used from a dataset.
            max_samples=1,
            weight=1,  # sampling weight during training
        )
        # train config is used to combined both configurations
        config = du.DatasetConfig(pathfinder, train_options)
        configs.append(config)

    pathfinder = du.Pathfinder(
        videoset="singapore", camera=annotated_singapore[-1], cache_dir=cache_dir
    )
    train_options = du.TrainOptions(
        val=True,
        offset_scales=[1],
        max_samples=3,
    )
    config = du.DatasetConfig(pathfinder, train_options)
    configs.append(config)
    return configs


# %%
