# #%%
from pathlib import Path

import pandas as pd
from loguru import logger
from tqdm import tqdm
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates

# from videosets_ii import Vi
from videosets_ii.videosets_ii import VideosetsII

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
names = list(videosets.to_pandas()["name"])
names = [x for x in names if "mantis" in x]


# %%
def get_result_options(mm):
    result_options = set()
    for video_info in mm._video_infos:
        result_dirpath_parts = len(video_info.result_dirpath.parts)
        results = video_info.result_dirpath.glob("**/*.csv")
        for x in results:
            result_item = "/".join(x.parts[result_dirpath_parts:])
            result_options.add(result_item)

    return list(result_options)


# datasets = prompt(names,True,'select videoset')
sets = []

types = ""


def make_constant(string: str):
    return (
        string.upper()
        .replace("-", "_")
        .replace("/", "_")
        .replace(" ", "_")
        .split(".")[0]
    )


for dataset in names:
    print(dataset)
    vset = videosets[dataset]
    cameras = vset.cameras
    options = []
    for camera in tqdm(cameras):
        try:
            mm = vset.get_mediamanager(camera)
            options += get_result_options(mm)
        except:
            logger.warning(f"{camera} failed")
        break
    options = list(set(options))

    qualities = []
    template = f"""
class {make_constant(dataset)}:
	NAME="{dataset}"
"""
    for camera in cameras:
        template += f'	CAM_{make_constant(camera)}="{camera}"\n'
    for option in options:
        template += f'	RESULT_{make_constant(option)}="{option}"\n'
    types += template
    # add detections as well?
    # And check availabilty of detections?

# print(types)
with open("vset_types.py", "w") as f:
    f.write(types)
# import vset_types as t

# print(t.MANTIS_2023.NAME)
# print(t.MANTIS_20230414_4PERSONS.CAM_EO_OVERVIEW)
