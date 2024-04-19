from media_manager.core import MediaManager
import os
from pathlib import Path
from loguru import logger
from videosets_ii.videosets_ii import VideosetsII
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath= basedirpath)#basedirpath)
videoset_names = list(videosets.to_pandas()['name'])

def find_result_csv_in_mm_path(self, mm):
    paths = list(mm.result_dirpath.rglob("*.csv"))
    # sorted_paths = sorted(paths, key=get_modified_date)
    path_options = [f"{x.parent.stem}/{x.name}" for x in paths]
    return path_options

def 
