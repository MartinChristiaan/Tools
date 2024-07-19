from dataclasses import dataclass
import os
from pathlib import Path
import pickle
from typing import List
import cv2
from videosets_ii.videosets_ii import VideosetsII
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
    cameras : List[str] = None
    detections_sources: List[str] = None
    selected_sources: List[str] = None
    annotation_suffix: str = "smallObjectsCorrected"
    pivot_columns: List[str] = None
    pivot_column_options: List[str] = None
    color = ""
    plotmode: str = "markers"  # can also be set to lines
    selected_detection: List[float] = None
    comment: str = ""
    y_axis_label: str = "bbox_x"

    @property
    def videoset_obj(self):
        return videosets[self.videoset]

    # @property
    # def cameras(self):
    #     return self.videoset_obj.cameras

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def set_videoset_data(self, data):
        if self.videoset != data["videoset"]:
            self.videoset = data["videoset"]
            self.cameras = [x for x in videosets[self.videoset].cameras if 'halfres' in x]
            # self.cameras = videosets[self.videoset].cameras
            self.camera = self.cameras[0]
            self.update_mm()

        elif self.camera != data["camera"]:
            self.camera = data["camera"]
            self.update_mm()

        elif self.selected_sources != data["selected_sources"]:
            self.selected_sources = data["selected_sources"]
            self.detections = self.load_detections()

        self.plotmode = data["plotmode"]
        self.pivot_columns = [
            x for x in data["groupbys"] if x in self.pivot_column_options
        ]
        self.color = data["color"]

    def update_mm(self):
        self._media_manager = videosets[self.videoset].get_mediamanager(self.camera)
        self.detections_sources = self.find_result_csv_in_mm_path(self.media_manager)
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
        if os.path.exists(self.frame_filename(offset, timestamp)):
            return cv2.imread(self.frame_filename(offset, timestamp))
        # TODO auto cachcing?
        return self.media_manager.get_frame(timestamp)

    def get_detections(self, timestamp):
        return self.detections[self.detections.timestamp == timestamp]

    def load_detections(self):
        detections_list = []
        paths = list(self.media_manager.result_dirpath.rglob("*.csv"))
        for path in self.selected_sources:
            my_path = [x for x in paths if path in str(x)][0]
            detections = pd.read_csv(my_path)
            detections["source"] = [path] * len(detections)
            detections_list.append(detections)

        if len(detections_list) > 0:
            df = pd.concat(detections_list)
            self.pivot_column_options = [str(x) for x in df.columns]
            return df

        self.pivot_column_options = []
        return None

    def find_result_csv_in_mm_path(self, mm):
        paths = list(mm.result_dirpath.rglob("*.csv"))
        sorted_paths = sorted(paths, key=get_modified_date)
        path_options = [f"{x.parent.stem}/{x.name}" for x in sorted_paths]
        return path_options

    @staticmethod
    def load(path):
        manager = IOData()
        with open(path, "rb") as f:
            data = pickle.load(f)
        for k, v in data.items():
            manager.__dict__[k] = v
        manager.update_mm()
        return manager

    def get_xt_plot(self, source):
        data = self.detections
        data = data[data.source == source]
        if len(self.pivot_columns) == 0:
            datadict = dict(
                x=list(data.timestamp),
                y=list(data.bbox_x),
                type="scatter",
                mode=self.plotmode,
                name="bbox_x",
            )
            if self.color != "":
                datadict.update(
                    {
                        "marker": {
                            "color": list(data[self.color]),
                            "colorscale": "Jet",
                        }
                    }
                )
            return [datadict]

        else:
            datas = []
            for groups, groupdf in data.groupby(self.pivot_columns):
                datadict = dict(
                    x=list(groupdf.timestamp),
                    y=list(groupdf.bbox_x),
                    type="scatter",
                    mode=self.plotmode,
                    name=",".join([str(x) for x in groups]),
                )
                # if self.color != "":
                #     datadict.update({"color": list(data[self.color])})
                datas.append(datadict)
            return datas

    # def save_annotations(self):
    #     self.media_manager.save_annotations()

    # save annotations to tmp annotation file on diskstation...
    # save annoatiation to diskstations
