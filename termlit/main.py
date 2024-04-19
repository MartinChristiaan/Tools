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


def multi_select(options: List[str]):
	if len(options) == 0:
		logger.warning('no options available')
		return None
	current_pattern = ""
	while True:
		selected = []
		for sub_pattern in current_pattern.split("+"):
			selected += fnmatch.filter(options, f"*{sub_pattern}*")

		print(current_pattern + " : ")
		print(",".join(selected))
		char = click.getchar()
		if char == 'space':


