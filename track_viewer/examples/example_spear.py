import os

from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks

from media_manager.core import MediaManager
from guitoolbox.app import SyncMode, MainGUI

dirname = r'C:\Users\leeuwenmcv\Downloads\20230612T140302_jeroen_volgend'
mm = MediaManager(os.path.join(dirname,r'video\EO'),
                  result_dirpath=os.path.join(dirname,r'\results\EO'),
                  video_suffix='.avi', log_column_to_use=0)

tracks = Tracks.load(os.path.join(dirname,r'results\tracks\tracks_live.csv'))
detections = Detections.load(os.path.join(dirname,r'results\detections\detections_EO_live.csv'))


# GUI
gui = MainGUI(
        videos=[mm],
        tracks=[tracks],
       sync_mode=SyncMode.ALL,
    )
