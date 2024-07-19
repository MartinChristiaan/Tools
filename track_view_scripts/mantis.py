cameras_eval = [
    "20231222T083009_crontab_recording/EO_zoom_half",
    "20231014T143008_crontab_recording/EO_zoom_half",
    "20231224T090009_crontab_recording/EO_zoom_half",
    "20231228T090009_crontab_recording/EO_zoom_half",
    "20231126T090009_crontab_recording/EO_zoom_half",
    "20231202T143009_crontab_recording/EO_zoom_half",
    "20230923T193008_crontab_recording/EO_zoom_half",
    "20231012T090008_crontab_recording/EO_zoom_half",
    "20231013T080008_crontab_recording/EO_zoom_half",
    "20230923T143008_crontab_recording/EO_zoom_half",
    "20231024T083009_crontab_recording/EO_zoom_half",
    "20231105T090008_crontab_recording/EO_zoom_half",
    "20230827T093008_crontab_recording_person_rainy/EO_zoom_half",
    "20231222T110010_crontab_recording/EO_zoom_half",
    "20230918T174658_crontab_recording_handmatig_regen_rainy/EO_zoom_half",
    "20230310T163009_crontab_recording_person_rainy_windy_snowy/EO_zoom_half",
    "20231212T140009_crontab_recording/EO_zoom_half",
    "20231118T103009_crontab_recording/EO_zoom_half",
    "20231120T103009_crontab_recording/EO_zoom_half",
    "20231125T143009_crontab_recording/EO_zoom_half",
    "20230401T121510_crontab_recording_person_rainy/EO_zoom_half",
]

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
videoset = VideosetsII()["mantis_2023"]
idx = 1
cam = cameras_eval[idx]
cam = "20230918T174658_crontab_recording_handmatig_regen_rainy/EO_zoom_half"
mm = videoset.get_mediamanager(cam)
# load tracks tyolo
tracks_tyolo = Detections(mm.load("tyolov8/detections_tyolov8m-30112023.csv"))
# GUI
gui = MainGUI(
    videos=[
        VideoView.Settings(
            video_model=MediaManagerModel(mm),
            linewidth=2,
            title="Detection yolo retrained",
        ),
    ],
    tracks=[
        TrackView.Settings(
            tracks_model=TrackerToolboxModel(tracks_tyolo),
            linewidth=1.5,
            color_map=ColorMap(8, palette="husl"),
            title="retrained",
        ),
    ],
    sync_mode=SyncMode.ALL,
)
