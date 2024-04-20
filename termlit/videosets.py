from pathlib import Path
from dataclasses import dataclass
from videosets_ii.videosets_ii import VideosetsII

from selection import (
    Menu,
    MenuItem,
    MenuItemBool,
    MenuItemMultiStr,
    MenuItemFloat,
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
        for videoset in videoset_selector.selected:
            self.options += videosets[videoset].cameras
        return super().select()


videoset_selector = MenuItemMultiStr("videosets", _selected=[], options=videoset_names)
camera_selector = CameraSelector(
    "camera", _selected=[], options=None, videoset_selector=videoset_selector
)
menu_items = [
    videoset_selector,
    camera_selector,
    MenuItemMultiStr("experiments", _selected=[], options=["proposed", "clipped"]),
    MenuItemBool("use tensorrt", True),
    MenuItemFloat("confidence", 0.1),
]
result = Menu(menu_items, "processing_app").run()
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
    item = MenuItem("videoset_camera", videoset_cameras)
    print(item.select())
