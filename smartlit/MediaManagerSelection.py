from Container import Container
from SelectBoxObservable import SelectBoxObservable
from main import default_cam, default_cams, default_vset, videosets

from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
from pathlib import Path
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
default_vset = "drone_detection_dataset_2021"
default_cams = videosets[default_vset].cameras
default_cam = videosets[default_vset].cameras[5]


class MediaManagerSelection(Container):
    def __init__(self) -> None:
        self.videoset = SelectBoxObservable(
            default_vset,
            "videoset",
            uimode="selectbox",
            options=list(videosets.to_pandas()["name"]),
        )
        self.camera = SelectBoxObservable(
            default_cam, "camera", uimode="selectbox", options=default_cams
        )
        self.videoset.subscribe(self.on_videoset_update)
        self.videosets = videosets
        super().__init__("Media Manager Selection")

    def on_videoset_update(self):
        cur_vset = self.videoset.value
        self.camera.options = self.videosets[cur_vset].cameras
        self.camera.set_value(self.camera.options[0])
