from multiprocessing import Queue
from pathlib import Path
from dataclasses import dataclass
import time
from videosets_ii.videosets_ii import VideosetsII

from termlit.selection import (
    Menu,
    MenuItem,
    MenuItemBool,
    MenuItemMultiStr,
    MenuItemFloat,
    QueueControl,
    TaskProcessor,
)

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


# camera_lut = []
# for vset in videoset_names:
#     camera_lut] += [vset + "|" + cam for cam in videosets[vset].cameras]
videoset_cameras = get_videoset_cameras(videoset_names)


@dataclass
class CameraSelector(MenuItemMultiStr):
    videoset_selector: MenuItemMultiStr = None

    def select(self):
        self.options = []
        for videoset in self.videoset_selector.selected:
            self.options += videosets[videoset].cameras
        return super().select()


videoset_selector = MenuItemMultiStr("videosets", _selected=[], options=videoset_names)
camera_selector = CameraSelector(
    "camera", _selected=[], options=None, videoset_selector=videoset_selector
)

if __name__ == "__main__":
    # from termlit.selection import TaskProcessor

    # def task(config):
    #     print(f"running {config}")
    #     time.sleep(600)

    # processor = TaskProcessor(task)

    menu_items = [
        videoset_selector,
        camera_selector,
        MenuItemMultiStr("experiments", _selected=[], options=["proposed", "clipped"]),
        MenuItemBool("use tensorrt", True),
        MenuItemFloat("confidence", 0.1),
        # QueueControl("queue", processer=processor),
    ]
    # while True:
    items = Menu(menu_items, "processing_app").run()
    import pandas as pd

    df = pd.DataFrame(items)
    df.to_csv("processing_app.csv")
