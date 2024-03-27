# %%
# %load_ext autoreload
# %autoreload 2
# Require


# Streamlit, select config + show xt_plot?

import argparse
import pickle
from pathlib import Path

import click
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

parser.add_argument("-s", "--start_idx", type=int, default=0)
parser.add_argument("-n", "--num_items", type=int, default=100)
args = parser.parse_known_args()[0]

datasets = all_configs
names = fnmatch.filter([x.pathfinder.name for x in datasets], args.config)
datasets = [x for x in datasets if x.pathfinder.name in names][::-1]


def export_fn(config: du.DatasetConfig):
    writer = writers[args.writer]
    writer(config, [0, -15, 15], label_config).write()


action_lut = dict(export=export_fn, annotate=BoundingBoxAnnotator.annotate_config)
for action in args.action.split(","):
    for d in datasets[args.start_idx : args.start_idx + args.num_items]:
        prev_annotations = d.pathfinder.media_manager.load_annotations(
            "smallObjectsCorrected"
        )
        data = []
        if not prev_annotations is None:
            continue
        action_lut[action](d)
        # if click.getchar() == "y":
        #     print("saving")
        #     tmp_path = d.pathfinder.annotations_path.with_suffix(".tmp.csv")
        #     if tmp_path.exists():
        #         annotations = pd.read_csv(tmp_path)
        #     # mm = d.pathfinder.media_manager.
        #     d.pathfinder.media_manager.save_annotations(
        #         annotations, "smallObjectsCorrected", True
        #     )
        #     print("saved new annotations")
