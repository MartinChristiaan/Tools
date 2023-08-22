import os

from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks

from media_manager.core import MediaManager
from guitoolbox.app import SyncMode, MainGUI

from utils.dataframe_utils import update_csv_with_dataclass

from dataclasses import dataclass
@dataclass
class TrackViewerConfig:
	videodir: str
	resultsdir : str
	detections_path:str
	tracks_path:str
	video_suffix:str
	log_column:int
	@staticmethod
	def from_df(df):
		return [TrackViewerConfig(**row) for i,row in df.iterrows()]

df =update_csv_with_dataclass(TrackViewerConfig,"spear.csv")
cfgs=  TrackViewerConfig.from_df(df)
for cfg in cfgs:
	print(cfg.__dict__)
	mm = MediaManager(cfg.videodir,
			result_dirpath=cfg.resultsdir,
			video_suffix=cfg.video_suffix, 
   			log_column_to_use=cfg.log_column)
	tracks = Tracks.load(cfg.tracks_path)
	gui = MainGUI(
		videos=[mm],
		tracks=[tracks],
	sync_mode=SyncMode.ALL,
	)
