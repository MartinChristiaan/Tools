from dataclasses import dataclass
import os
from pathlib import Path
from typing import List
import cv2
from loguru import logger

from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
import pandas as pd
import dlutils_ii as du
from dlutils_ii.dataset_cache.pathfinder import read_logfile

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
names = list(videosets.to_pandas()["name"])


def get_modified_date(path):
    return os.path.getmtime(path)


@dataclass
class IOData(du.Pathfinder):
    detections_sources: List[str] = None
    selected_sources: List[str] = None
    annotation_suffix: str = "smallObjectsCorrected"

    @property
    def videoset_obj(self):
        return videosets[self.videoset]

    @property
    def cameras(self):
        return self.videoset_obj.cameras

    def to_dict(self):
        return dict(
            videoset=self.videoset,
            camera=self.camera,
            cameras=self.cameras,
            videosets=names,
            sources=[str(x) for x in self.detections_sources],
            selected_source=[str(x) for x in self.selected_sources],
            cached_timestamps=read_logfile(self.logfile_path),
        )

    def set_videoset_data(self, data):
        if self.videoset != data["videoset"]:
            self.videoset = data["videoset"]
            self.cameras = videosets[self.videoset].cameras
            self.camera = self.cameras[0]
            self.update_mm()

        elif self.camera != data["camera"]:
            self.camera = self.cameras[0]
            self.update_mm()

        elif self.selected_sources == data["selected_sources"]:
            self.detections = self.load_detections()

    def update_mm(self):
        self._media_manager = videosets[self.videoset].get_mediamanager(self.camera)
        self.detections_sources = self.load_path_from_mediamanager(self.mm)
        self.selected_sources = [
            source
            for source in self.selected_sources
            if source in self.detections_sources
        ]
        self.detections = self.load_detections()

    @property
    def timestamps(self):
        return self.media_manager.timestamps

    def get_frame(self, timestamp, offset):
        if os.path.exists(self.frame_filename, offset):
            return cv2.imread(self.frame_filename)
        # TODO auto cachcing?
        return self.media_manager.get_frame(timestamp)

    def get_detections(self, timestamp):
        return self.detections[self.detections.timestamp == timestamp]

    def load_detections(self):
        detections_list = []
        for path in self.selected_sources:
            from_supra = "_supra" in path
            detections = self.mm.load(path.replace("_supra/", ""), from_supra)
            detections["source"] = path
            detections_list.append(detections)
        if len(detections_list) > 0:
            return pd.concat(detections_list)
        return None

    def load_path_from_mediamanager(self, mm):
        paths = list(mm.result_dirpath.rglob("*.csv"))
        sorted_paths = sorted(paths, key=get_modified_date)
        path_options = [f"{x.parent.stem}/{x.name}" for x in sorted_paths]
        return path_options

    # save annotations to tmp annotation file on diskstation...
    # save annoatiation to diskstations
