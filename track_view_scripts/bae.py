from videosets_ii.videosets_ii import VideosetsII
import numpy as np

from guitoolbox.app import SyncMode, MainGUI
from guitoolbox.models.media_manager import MediaManagerModel
from guitoolbox.models.tracker_toolbox import TrackerToolboxModel
from guitoolbox.views.video import VideoView
from guitoolbox.views.track import TrackView
from guitoolbox.visualize import ColorMap

from trackertoolbox.tracks import TrackUpdates
from trackertoolbox.tracker import BboxTracker
from trackertoolbox.detections import Detections

# get videoset and mediamanager
videoset = VideosetsII()["bae_cv90_2023"]
mm = videoset.get_mediamanager("UAV_1000/UAV_1000-EOPS_IR_N")

# load tracks tyolo
tracks_tyolo = Detections(mm.load("tyolov8/detections_tyolov8m-30112023.csv"))
# GUI
gui = MainGUI(
    videos=[
        VideoView.Settings(
            video_model=MediaManagerModel(mm), linewidth=2, title="Tracks tyolo"
        ),
    ],
    tracks=[
        TrackView.Settings(
            tracks_model=TrackerToolboxModel(tracks_tyolo),
            linewidth=1.5,
            color_map=ColorMap(8, palette="husl"),
            title="Tracks tyolo",
        ),
    ],
    sync_mode=SyncMode.ALL,
)
