from Container import Container
from SelectBoxObservable import SelectBoxObservable
from main import default_cam, default_cams, default_vset, videosets

from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
from pathlib import Path
import pandas as pd

from state import Observable

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)
default_vset = "drone_detection_dataset_2021"
default_cams = videosets[default_vset].cameras
default_cam = videosets[default_vset].cameras[5]


def find_result_csv_in_mm_path(mm):
    paths = list(mm.result_dirpath.rglob("*.csv"))
    sorted_paths = sorted(paths, key=get_modified_date)
    # path_options = [f"{x.parent.stem}/{x.name}" for x in sorted_paths]
    return sorted_paths


import os


def get_modified_date(path):
    return os.path.getmtime(path)


class PlotData(Observable):
    def __init__(self, df, x_axis_label, y_axis_label, pivot_column) -> None:
        self.value = df
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.pivot_column = pivot_column
        self.plot_type = "scatter"

    def get_ui_data(self):
        data = self.value
        if len(data) == 0:
            return {}

        if self.plot_type == "scatter":
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
            for groups, groupdf in data.groupby(self.pivot_column):
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


class MediaManagerSelection(Container):
    def __init__(self) -> None:
        self.videoset = SelectBoxObservable(
            default_vset,
            "videoset",
            uimode="selectbox",
            options=list(videosets.to_pandas()["name"]),
        )
        self.camera = SelectBoxObservable(
            default_cam, "camera", uimode="selectbox", options=default_cams
        )
        self.videosets = videosets
        self.mm = videosets[self.videoset.value].get_mediamanager(self.camera.value)

        self.videoset.subscribe(self.on_videoset_update)
        self.camera.subscribe(self.on_camera_update)
        self.data_table_path = SelectBoxObservable("", options=[])
        self.data_table = Observable(pd.DataFrame(), "data_table")
        super().__init__("Media Manager Selection")

    def on_videoset_update(self):
        cur_vset = self.videoset.value
        self.camera.options = self.videosets[cur_vset].cameras
        self.camera.set_value(self.camera.options[0])

    def on_camera_update(self):
        self.mm = videosets[self.videoset.value].get_mediamanager(self.camera.value)
        self.data_table.options = find_result_csv_in_mm_path(self.mm)

    def on_data_table_update(self):
        df = self.mm.load(self.data_table.value)
