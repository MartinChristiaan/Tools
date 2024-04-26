from typing import Any
from state import Observable

import os
from pathlib import Path
from loguru import logger

from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks,TrackUpdates
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath= basedirpath)#basedirpath)
default_vset = 'drone_detection_dataset_2021'
default_cams=  videosets[default_vset].cameras
default_cam=  videosets[default_vset].cameras[5]

class MediaManagerSelection:
	def __init__(self) -> None:
		self.videoset = Observable(default_vset,'videoset')
		self.camera_options = Observable(default_cams,'videoset')
		self.camera = Observable(default_cam,'camera')
		self.videoset.subscribe(self.on_videoset_update)

	def on_videoset_update(self):
		self.camera_options.set_value(videosets[self.videoset.value].cameras)
	
	
