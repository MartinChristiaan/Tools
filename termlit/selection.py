# import os
# from pathlib import Path
# from loguru import logger

# from videosets_ii.videosets_ii import VideosetsII
# from trackertoolbox.detections import Detections
# from trackertoolbox.tracks import Tracks,TrackUpdates
# import pandas as pd

# basedirpath = Path(r"/diskstation")
# videosets = VideosetsII(basedirpath= basedirpath)#basedirpath)


from dataclasses import dataclass
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


@dataclass
class MenuItem:
    name: str
    options: List
    single_value: bool = False

    def select(self):
        if len(self.options) == 0:
            logger.warning(f"no options available for {self.name}")
            return None
        current_pattern = ""
        while True:
            selected = []
            for sub_pattern in current_pattern.split("+"):
                selected += fnmatch.filter(self.options, f"*{sub_pattern}*")
            if len(selected) == 0:
                current_pattern = ""
                continue
            click.clear()
            print(",".join(selected))
            print(f"Pattern : {current_pattern}")
            char = click.getchar()
            if char == " ":
                if self.single_value:
                    return selected[0]
                return selected
            current_pattern += char
