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
basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
names = list(videosets.to_pandas()["name"])


def get_modified_date(path):
    return os.path.getmtime(path)


@dataclass
class IOData(du.Pathfinder):
    detections_sources : List[str ] = None
    selected_sources : List[str ] = None
    @property
    def videoset_obj(self):
        return videosets[self.videoset]

    @property
    def cameras(self):
        return self.videoset_obj.cameras
        # self.cameras = videosets[self.videoset].cameras
        # # self.detections_sources = ["tracks/yolov8s_precision_20240301_resnet18.csv"]
        # self.mm = videosets[self.videoset].get_mediamanager(self.camera)
        # self.detections_sources = self.load_annotation_source(self.mm)
        # self.selected_sources = self.detections_sources[:1]
        # self.detections = self.load_detections()


    def to_dict(self):
        return dict(
            videoset=self.videoset,
            camera=self.camera,
            cameras=self.cameras,
            videosets=names,
            sources=[str(x) for x in self.detections_sources],
            selected_source=[str(x) for x in self.selected_sources],
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
        self.detections_sources = self.load_annotation_source(self.mm)
        self.selected_sources = [
            source
            for source in self.selected_sources
            if source in self.detections_sources
        ]
        self.detections = self.load_detections()

    @property
    def timestamps(self):
        return self.media_manager.timestamps

    def get_frame(self, timestamp,offset):
        if os.path.exists(self.frame_filename,offset):
            return cv2.imread(self.frame_filename)
        # TODO auto cachcing?
        return self.media_manager.get_frame(timestamp)

    def get_detections(self, timestamp):
        return self.detections[self.detections.timestamp == timestamp]

    def load_detections(self):
        detections_list = []
        for source in self.selected_sources:
            path = f"{source.parent.stem}/{source.name}"
            from_supra = "_supra" in path
            detections = self.mm.load(path.replace("_supra/", ""), from_supra)
            detections["source"] = source
            detections_list.append(detections)
        if len(detections_list) > 0:
            return pd.concat(detections_list)
        return None

    def load_annotation_source(self, mm):
        paths = list(mm.result_dirpath.rglob("*.csv"))
        sorted_paths = sorted(paths, key=get_modified_date)
        latest_path = [x for x in sorted_paths]
        return latest_path
