# %%
# Require
import argparse
import pickle
from pathlib import Path
from config.dataset import all_configs
import fnmatch
import dlutils_ii as du


parser = argparse.ArgumentParser(prog="ProgramName", description="Description")
parser.add_argument("-c", "--config", type=str, default="*DJI*")
parser.add_argument("-a", "--action", type=str, default="export")
args = parser.parse_known_args()[0]

datasets = all_configs
names = fnmatch.filter([x.pathfinder.name for x in datasets], args.config)
datasets = [x for x in datasets if x.pathfinder.name in names]
from functools import partial


action_lut = dict(
    export=partial(
        du.Writer.export_from_config,
        frame_offsets=[0, -15, 15],
        label_config=du.LabelConfig(),
    ),
)
for action in args.action.split(","):
    for d in datasets:
        action_lut[action](d)
