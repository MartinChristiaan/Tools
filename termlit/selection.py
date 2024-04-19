# import os
# from pathlib import Path
# from loguru import logger

# from videosets_ii.videosets_ii import VideosetsII
# from trackertoolbox.detections import Detections
# from trackertoolbox.tracks import Tracks,TrackUpdates
# import pandas as pd

# basedirpath = Path(r"/diskstation")
# videosets = VideosetsII(basedirpath= basedirpath)#basedirpath)


from typing import List
import click

import fnmatch
from loguru import logger


def flatten_list(list_of_lists):
    result = []
    for l in list_of_lists:
        for x in l:
            result.append(x)
    return result


def select(options: List[str], name="selector"):
    if len(options) == 0:
        logger.warning(f"no options available for {name}")
        return None
    current_pattern = ""
    while True:
        selected = []
        for sub_pattern in current_pattern.split("+"):
            selected += fnmatch.filter(options, f"*{sub_pattern}*")
        if len(selected) == 0:
            current_pattern = ""
            continue
        click.clear()
        print(f"Pattern : {current_pattern}")
        print(",".join(selected))
        char = click.getchar()
        if char == " ":
            return selected
        current_pattern += char
