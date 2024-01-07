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
from media_manager.core import MediaManager
from pathlib import Path

root = Path("/mnt/dl-41/data/leeuwenmcv/diskstation/webcams_2023/video/")
cams = list(root.glob("*"))
cams.sort()
print(cams)
sequences = []

# get videoset and mediamanager
# for cam in cams:
mm = MediaManager(cams[7], video_suffix=".mp4")
# load tracks tyolo
tracks_tyolo = Detections(mm.load("tyolov8/detections_finetuned.csv"))
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
