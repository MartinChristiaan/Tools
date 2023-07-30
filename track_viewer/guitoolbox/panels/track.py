import functools
from typing import Sequence

from PySide6.QtWidgets import QVBoxLayout, QLabel

from guitoolbox.visualize import ColorMap
from guitoolbox.views import track
from guitoolbox.models.base import TrackModel
from guitoolbox.panel import Panel


class TrackPanel(Panel):
    def __init__(
        self,
        tracks_model: TrackModel,
        color_map: ColorMap,
        timestamp_min: float,
        timestamp_max: float,
        name: str = "TrackPanel",
    ) -> None:
        super().__init__(name)

        self.tracks_model = tracks_model
        self.color_map = color_map

        self._listen_to = set()

        # Create layout with labels
        self.hbox_layout = QVBoxLayout()
        self.label1 = QLabel(self.name)  # NOTE leave this line here! deleting it seems to break app...
        # NOTE: use "track.TrackView" instead of TrackView. This allows monkey patching, see "example_annotation.py"
        self.track_view = track.TrackView(
            timestamp_min,
            timestamp_max,
            self.tracks_model,
            color_map,
            on_timestamp_changed=functools.partial(self.set_timestamp, source=self.name),
        )  # NOTE leave this line here! moving it seems to break app...
        self.hbox_layout.addWidget(self.track_view)
        self.setLayout(self.hbox_layout)

        self.timestamp = timestamp_min

    def setup(self):
        self.set_timestamp(timestamp=self.timestamp, source=self.name)

    def listen_to(self, source: Sequence[str]) -> None:
        self._listen_to.update(set(source) - {self.name})

    def update_panel(self, source_name: str, data: dict):
        if source_name in self._listen_to and "timestamp" in data:
            timestamp = float(data["timestamp"])
            self.set_timestamp(timestamp, source_name)

    def set_timestamp(self, timestamp: float, source: str):
        self.timestamp = timestamp

        self.track_view.set_timestamp(timestamp)

        if source == self.name:
            self.publish_timestamp()

    def publish_timestamp(self):
        self.publish({"name": self.name, "timestamp": self.timestamp})
