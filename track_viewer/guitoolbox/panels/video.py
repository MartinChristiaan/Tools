from typing import Optional, Sequence

import numpy as np
from guitoolbox.models.base import TrackModel, VideoModel
from guitoolbox.panel import Panel
from guitoolbox.views.video import VideoView
from guitoolbox.visualize import ColorMap
from PySide6.QtWidgets import QVBoxLayout


class VideoPanel(Panel):
    def __init__(
        self,
        video_model: VideoModel,
        tracks_model: Optional[TrackModel] = None,
        color_map: Optional[ColorMap] = None,
        name: str = "VideoPanel",
    ) -> None:
        super(VideoPanel, self).__init__(name)

        self.video_model = video_model
        self.tracks_model = tracks_model
        self._listen_to = set()

        # Create layout with labels
        self.hbox_layout = QVBoxLayout()
        self.video_view = VideoView(
            self.video_model, self.tracks_model, color_map
        )  # NOTE leave this line here! moving it seems to break app..
        self.hbox_layout.addWidget(self.video_view)
        self.setLayout(self.hbox_layout)

        self.timestamp = 0.0

    def setup(self):
        timestamp = self.video_model.timestamps_first()
        self.set_timestamp(timestamp=timestamp, source=self.name)

    def listen_to(self, source: Sequence[str]) -> None:
        self._listen_to.update(set(source) - {self.name})

    def update_panel(self, source_name: str, data: dict):
        if source_name in self._listen_to and "timestamp" in data:
            timestamp = float(data["timestamp"])
            self.set_timestamp(timestamp, source_name)

    def set_timestamp(self, timestamp: float, source: str):
        if abs(timestamp - self.timestamp) <= 0.00001:
            return  # Prevents recursion
        self.timestamp = self.video_view.set_timestamp(timestamp)

        if source == self.name:
            self.publish_timestamp()

    def publish_timestamp(self):
        self.publish({"name": self.name, "timestamp": self.timestamp})
