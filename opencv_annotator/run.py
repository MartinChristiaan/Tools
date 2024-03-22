# %%
# Require
import argparse
import pickle
from pathlib import Path
from config.dataset import all_configs
import fnmatch

parser = argparse.ArgumentParser(prog="ProgramName", description="Description")
parser.add_argument("-c", "--config", type=str, default="*DJI*")
args = parser.parse_known_args()[0]
datasets = all_configs
names = fnmatch.filter([x.pathfinder.name for x in datasets], args.config)
datasets = [x for x in datasets if x.pathfinder.name in names]
