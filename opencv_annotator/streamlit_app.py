# %%
# %load_ext autoreload
# %autoreload 2
# Require


# Streamlit, select config + show xt_plot?

import argparse
import pickle
from pathlib import Path

from loguru import logger
import pandas as pd
from config.dataset import all_configs
import fnmatch
import dlutils_ii as du

from opencv_annotator.annotator import BoundingBoxAnnotator
from config.writers import writers, label_config


parser = argparse.ArgumentParser(prog="ProgramName", description="Description")
parser.add_argument("-c", "--config", type=str, default="*TIE*")
parser.add_argument("-a", "--action", type=str, default="annotate")
parser.add_argument("-w", "--writer", type=str, default="tyolo_writer")

parser.add_argument("-s", "--start_idx", type=int, default=1)
parser.add_argument("-n", "--num_items", type=int, default=5)
args = parser.parse_known_args()[0]


datasets = all_configs
names = fnmatch.filter([x.pathfinder.name for x in datasets], args.config)
datasets = [x for x in datasets if x.pathfinder.name in names][::-1]


def export_fn(config: du.DatasetConfig):
    writer = writers[args.writer]
    writer(config, [0, -15, 15], label_config).write()


action_lut = dict(export=export_fn, annotate=BoundingBoxAnnotator.annotate_config)
for action in args.action.split(","):
    for d in datasets[args.start_idx : args.num_items]:
        action_lut[action](d)
