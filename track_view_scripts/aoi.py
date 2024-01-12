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
videoset = VideosetsII()["aot"]
for camera in videoset.cameras[:40]:
    mm = videoset.get_mediamanager(camera)
    # load tracks tyolo
    tracks_tyolo = Detections(mm.load("yolov8/detections_yolo_lowerbbox.csv"))
    tracks_pretrained = Detections(mm.load(f"detections/yolov5x_mscoco.csv"))
    # GUI
    gui = MainGUI(
        videos=[
            VideoView.Settings(
                video_model=MediaManagerModel(mm),
                linewidth=2,
                title="Detection yolo retrained",
            ),
            VideoView.Settings(
                video_model=MediaManagerModel(mm),
                linewidth=2,
                title="Detection yolo mscoco",
            ),
        ],
        tracks=[
            TrackView.Settings(
                tracks_model=TrackerToolboxModel(tracks_tyolo),
                linewidth=1.5,
                color_map=ColorMap(8, palette="husl"),
                title="retrained",
            ),
            TrackView.Settings(
                tracks_model=TrackerToolboxModel(tracks_pretrained),
                linewidth=1.5,
                color_map=ColorMap(8, palette="husl"),
                title="pretrained",
            ),
        ],
        sync_mode=SyncMode.ALL,
    )
