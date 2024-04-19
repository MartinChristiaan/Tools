from typing import List
from media_manager.core import MediaManager
import os
from pathlib import Path
from loguru import logger
from itertools import product
import numpy as np
from videosets_ii.videosets_ii import VideosetsII
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
videoset_names = list(videosets.to_pandas()["name"])


def find_result_csv_in_mm_path(self, mm):
    paths = list(mm.result_dirpath.rglob("*.csv"))
    # sorted_paths = sorted(paths, key=get_modified_date)
    path_options = [f"{x.parent.stem}/{x.name}" for x in paths]
    return path_options


def get_cameras(videoset_names):
    cameras = []
    for vset in videoset_names:
        cameras += videosets[vset].cameras
    return cameras


def get_videoset_cameras(videoset_names):
    cameras = []
    for vset in videoset_names:
        cameras += [vset + "|" + cam for cam in videosets[vset].cameras]
    return cameras


from selection import MenuItemStringList, menu

videoset_cameras = get_videoset_cameras(videoset_names)
menu_items = [
    MenuItemStringList("experiments", ["proposed", "clipped"]),
    MenuItemStringList("MM", videoset_cameras),
    MenuItemStringList("use tensorrt", [True, False]),
    MenuItemStringList("confidence", np.linspace(0, 1, 100)),
]
result = menu(menu_items, "processing_app")
print(result)


# def videoset_camera_selection():
#     vsets = select(videoset_names)
#     cameras = get_cameras(vsets)
#     cameras = select(cameras)
#     results = []
#     for camera, vset in product(cameras, vsets):
#         if camera in videosets[vset].cameras:
#             results.append((vset, camera))
#     return results


# def menu(menuitems : List[MenuItem]):

# current_config = {"videoset_cameras": [], "experiments": [], "use_tensorrt": False}


if __name__ == "__main__":
    item = MenuItemStringList("videoset_camera", videoset_cameras)
    print(item.select())
