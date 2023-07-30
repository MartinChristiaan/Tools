from typing import Optional

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from guitoolbox.visualize import ColorMap, DetectionRectangle
from guitoolbox.models.base import VideoModel, TrackModel


class VideoView(FigureCanvasQTAgg):
    def __init__(
        self,
        video_model: VideoModel,
        tracks_model: Optional[TrackModel] = None,
        color_map: Optional[ColorMap] = None,
        width: int = 12,
        height: int = 10,
        dpi: int = 100,
    ):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout(pad=0)
        self.axes = fig.add_subplot(111)  # Use these self.axes to interact with the plot
        super(VideoView, self).__init__(fig)

        self.video_model = video_model
        self.tracks_model = tracks_model
        self.color_map = color_map

        self.frame = None
        self.timestamp = None
        self.frame_clear()

    def set_timestamp(self, timestamp: float) -> float:
        if timestamp in self.video_model:
            frame, timestamp = self.video_model[timestamp]
            self.frame_set(frame, timestamp)
        else:
            self.frame_clear()
        self.timestamp = timestamp

        return self.timestamp

    def frame_set(self, frame: np.ndarray, timestamp: float):
        self.frame = frame
        self.timestamp = timestamp
        self.frame_draw()

    def frame_clear(self):
        self.frame = np.zeros(shape=(300, 300, 3), dtype=np.uint8)
        self.timestamp = 0.0
        self.frame_draw()

    def frame_draw(self):
        self.axes.cla()
        # Draw frame
        self.axes.imshow(self.frame)
        self.axes.axis("off")

        # Draw detections
        if self.tracks_model is not None:
            detections = self.tracks_model.detections_by_timestamp(self.timestamp)
            if detections is not None:
                self.plot_detections(
                    detections,
                    self.color_map,
                    self.axes,
                    fill=False,
                    picker=True,
                )
        self.draw()

    def plot_detections(
        self,
        detections: pd.DataFrame,
        color_map: ColorMap,
        axes: Axes = None,
        **kwargs,
    ):
        if axes is None:
            fig, axes = plt.subplots()
        for idx, track in detections.iterrows():
            kwargs["edgecolor"] = color_map[int(track["track_id"])]
            rectangle = DetectionRectangle(
                xy=(track["bbox_x"], track["bbox_y"]),
                width=track["bbox_w"],
                height=track["bbox_h"],
                **kwargs,
            )
            rectangle.metadata = track
            axes.add_patch(rectangle)
