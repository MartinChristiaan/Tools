# %%
from pathlib import Path

import pandas as pd
from loguru import logger
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
from videosets_ii.videosets_ii import VideosetsII

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
names = list(videosets.to_pandas()["name"])
print(names)


# mantis = [x for x in names if 'mantis' in x]
# %%
from media_manager.core import MediaManager


def get_result_options(mm: MediaManager):
    result_options = set()
    for video_info in mm._video_infos:
        result_dirpath_parts = len(video_info.result_dirpath.parts)
        results = video_info.result_dirpath.glob("**/*.csv")
        for x in results:
            result_item = "/".join(x.parts[result_dirpath_parts:])
            result_options.add(result_item)

    result_options = list(result_options)


videoset = "dji_20230928_Walaris"
vset = videosets.get_videoset(videoset)
for camera in vset.cameras:
    mm = vset.get_mediamanager(camera)
    get_result_options(mm)


# %%
