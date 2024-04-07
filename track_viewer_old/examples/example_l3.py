from guitoolbox.app import MainGUI, SyncMode
from media_manager.core import MediaManager
from trackertoolbox.detections import Detections
from trackertoolbox.tracker import BboxTracker

# get mediamanager object
mm = MediaManager(
    r"\\diskstationii1.tsn.tno.nl\meoss\data\20180225_ijmuiden_L3\video\Visueel",
    result_dirpath=r"\\diskstationii1.tsn.tno.nl\meoss\data\20180225_ijmuiden_L3\results\Visueel",
    video_suffix=".avi",
)

# load detections
det = mm.load("yolov5x_mscoco.csv")
detections = Detections(det)

# only one class (example)
detections2 = detections[detections.label == "kite"]

# tracker
tracker = BboxTracker(
    cost_max=0.8,  # default is 0.8, hoger geeft minder tracks, 0.8 is misschien al redelijk hoog
    fps=10,  # liever een te lage fps dan een te hoge
    max_afterlife=2,  # hoeveel seconde een track mag blijven bestaan
)

# do tracking on fist 100000 detections
tracker.do_tracking(detections[0:100000], waitbar=True)

# get all tracks, only tracks > 10 detections
tracks = tracker.get_all_tracks()
tracks2 = tracks[
    tracks.len_tracks() > 10
]  # only tracks that are longer than 10 detections

# GUI
gui = MainGUI(
    videos=[mm],
    tracks=[tracks2],
    sync_mode=SyncMode.ALL,
)
