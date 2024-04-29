# %%
from typing import List

import pandas as pd
from Container import Container
from SelectBoxObservable import SelectBoxObservable
from videosets_ii.videosets_ii import VideosetsII
from pathlib import Path

from state import FuncStack, Observable, ObservableLogger

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
        super().__init__(df, name, check_if_same=False)

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
                    data=list(
                        zip(group_df[self.x_axis_label], group_df[self.y_axis_label])
                    ),
                )
            )
        return dict(series=series, plot_type=self.plot_type)

    def log_state(self, data):
        print(f"logging {self.name}, special")
        data[f"{self.name}_x_axis_label"] = self.x_axis_label
        data[f"{self.name}_y_axis_label"] = self.y_axis_label
        data[f"{self.name}_pivot_column"] = self.pivot_column
        return data
        print(data)


class MPLPlotter:
    def __init__(self, plot: Plot) -> None:
        self.plotobs = plot

    def plot(self):
        exec_cnt = FuncStack().exec_cnt
        plotdata = self.plotobs.get_ui_data()

        import matplotlib.pyplot as plt

        plt.figure()
        for series in plotdata["series"]:
            xdata = [x for x, y in series["data"]]
            ydata = [y for x, y in series["data"]]
            print(len(xdata))
            print(len(ydata))

            if plotdata["plot_type"] == "scatter":
                plt.scatter(xdata, ydata)
            if plotdata["plot_type"] == "line":
                plt.plot(xdata, ydata)
        plt.savefig(
            ObservableLogger().logdir
            / f"{self.plotobs.name}_{FuncStack().exec_cnt}.png"
        )


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
        self.data_table_path = SelectBoxObservable("", "data_table_path", options=[])
        self.data_table = Plot(pd.DataFrame(), "data_table", "timestamp", "bbox_x", "")

        self.on_camera_update()
        self.data_table_path._value = self.data_table_path.options[0]
        self.data_table_path.subscribe(self.on_data_table_path_update)
        self.on_data_table_path_update()
        super().__init__("Media Manager Selection")

    def get_observables(self) -> List[Observable]:
        return [self.videoset, self.camera, self.data_table_path]

    def on_videoset_update(self):
        cur_vset = self.videoset.value
        self.camera.options = self.videosets[cur_vset].cameras
        self.camera.set_value(self.camera.options[0])

    def on_camera_update(self):
        self.mm = videosets[self.videoset.value].get_mediamanager(self.camera.value)
        self.data_table_path.options = [
            f"{x.parent.stem}/{x.name}"
            for x in find_result_csv_in_mm_path(self.mm)
            if not "annotations" in str(x) or "temp" in str(x)
        ]
        self.data_table_path.set_value(self.data_table_path.options[0])

    def on_data_table_path_update(self):
        print(self.data_table_path.value)
        df = self.mm.load(self.data_table_path.value)
        print(df)
        self.data_table.set_value(df)


if __name__ == "__main__":
    mm_sel = MediaManagerSelection()
    # mm_sel.videoset.set_value("drone-tracking")
    mm_sel.videoset.set_value("drone_detection_dataset_2021")
    print(pd.read_csv(ObservableLogger().logfile).to_markdown())

    plotter = MPLPlotter(mm_sel.data_table)
    plotter.plot()
