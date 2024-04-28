from Container import Container
from SelectBoxObservable import SelectBoxObservable

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


class Plot(Observable):
    def __init__(self, df, name, x_axis_label, y_axis_label, pivot_column) -> None:
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.pivot_column = pivot_column
        self.plot_type = "scatter"
        super().__init__(df, name)

    def get_ui_data(self):

        base_df = self.value
        if len(base_df) == 0:
            return {}

        if len(self.pivot_column) == 0 or not self.pivot_column in base_df:
            df_groups = [(self.y_axis_label, base_df)]
        else:
            df_groups = [x for x in base_df.groupby(self.pivot_column)]

        series = []
        for group_name, group_df in df_groups:
            series.append(
                dict(
                    name=group_name,
                    data=zip(group_df[self.x_axis_label], group_df[self.y_axis_label]),
                )
            )
        return dict(series=series, plot_type=self.plot_type)


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
        self.data_table = Plot(pd.DataFrame(), "data_table", "timestamp", "bbox_x", "")
        self.data_table_path.subscribe(self.on_data_table_path_update)
        super().__init__("Media Manager Selection")

    def on_videoset_update(self):
        cur_vset = self.videoset.value
        self.camera.options = self.videosets[cur_vset].cameras
        self.camera.set_value(self.camera.options[0])

    def on_camera_update(self):
        self.mm = videosets[self.videoset.value].get_mediamanager(self.camera.value)
        self.data_table.options = find_result_csv_in_mm_path(self.mm)

    def on_data_table_path_update(self):
        self.data_table.set_value(self.mm.load(self.data_table_path.value))
