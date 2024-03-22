# %%
# Require
import argparse
import pickle
from pathlib import Path

from loguru import logger
import pandas as pd
from config.dataset import all_configs
import fnmatch
import dlutils_ii as du

from opencv_annotator.annotator import BoundingBoxAnnotator


parser = argparse.ArgumentParser(prog="ProgramName", description="Description")
parser.add_argument("-c", "--config", type=str, default="*TIE*")
parser.add_argument("-a", "--action", type=str, default="annotate")
args = parser.parse_known_args()[0]

datasets = all_configs
names = fnmatch.filter([x.pathfinder.name for x in datasets], args.config)
datasets = [x for x in datasets if x.pathfinder.name in names]
from functools import partial
from click import getchar


action_lut = dict(
    export=partial(
        du.Writer.export_from_config,
        frame_offsets=[0, -15, 15],
        labelconfig=du.LabelConfig(),
    ),
    annotate=BoundingBoxAnnotator.annotate_config,
)
for action in args.action.split(","):
    for d in datasets:
        action_lut[action](d)
