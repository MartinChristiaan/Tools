from trackertoolbox.tracker import BboxTracker
from trackertoolbox.detections import Detections

from media_manager.core import MediaManager
from guitoolbox.app import SyncMode, MainGUI

# get mediamanager object
mm = MediaManager(r'\\diskstationii1.tsn.tno.nl\meoss\data\20180225_ijmuiden_L3\video\Visueel',
                  result_dirpath=r'\\diskstationii1.tsn.tno.nl\meoss\data\20180225_ijmuiden_L3\results\Visueel',
                  video_suffix='.avi')

# load detections
det = mm.load("yolov5x_mscoco.csv")
detections = Detections(det)

# only one class (example)
detections2 = detections[detections.label == "kite"]

# GUI
gui = MainGUI(
    videos=[mm],
    tracks=[detections2],
    sync_mode=SyncMode.ALL,
)
