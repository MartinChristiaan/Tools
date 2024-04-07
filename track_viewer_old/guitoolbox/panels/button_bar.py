from typing import Sequence

import numpy as np
from guitoolbox.panel import Panel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QHBoxLayout, QPushButton


class ButtonBarPanel(Panel):
    def __init__(
        self,
        step_size_small: float,
        step_size_large: float,
        name: str = "ButtonBarPanel",
    ) -> None:
        super().__init__(name)

        self._listen_to = set()

        self.frame_timestamp = 0.0
        self.step_size_small = step_size_small
        self.step_size_large = step_size_large
        self.is_playing = False

        layout = QHBoxLayout()
        # btn = QPushButton("<<")
        # btn.pressed.connect(self.decrease_large)  # NOQA
        # layout.addWidget(btn)

        # btn = QPushButton("<")
        # btn.pressed.connect(self.decrease_small)  # NOQA
        # layout.addWidget(btn)

        # self.btn_play = QPushButton("Play")
        # self.btn_play.pressed.connect(self.play_pressed)  # NOQA
        # layout.addWidget(self.btn_play)

        # btn = QPushButton(">")
        # btn.pressed.connect(self.increase_small)  # NOQA
        # layout.addWidget(btn)

        # btn = QPushButton(">>")
        # btn.pressed.connect(self.increase_large)  # NOQA
        # layout.addWidget(btn)
        self.setLayout(layout)

        self.timestamp = 0.0

        self.timer = QTimer(self)
        self.timer.setInterval(self.step_size_small * 1000)
        self.timer.timeout.connect(self.on_play_update)  # NOQA

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Override QWidget keyPressEvent
        """
        print("key event from button bar")
        return super().keyPressEvent(event)

    def setup(self):
        pass  #

    def listen_to(self, source: Sequence[str]) -> None:
        self._listen_to.update(set(source) - {self.name})

    def update_panel(self, source_name: str, data: dict):
        if source_name in self._listen_to and "timestamp" in data:
            timestamp = float(data["timestamp"])
            self.set_timestamp(timestamp, source_name)
        elif source_name in self._listen_to and "play" in data:
            if data["play"] != self.is_playing:
                self.play_pressed()

    def set_timestamp(self, timestamp: float, source: str):
        if abs(timestamp - self.timestamp) <= 0.00001:
            return  # Prevents recursion
        self.timestamp = timestamp

        if source == self.name:
            self.publish_timestamp()

    def publish_timestamp(self):
        self.publish({"name": self.name, "timestamp": self.timestamp})

    def publish_play_status(self):
        self.publish({"name": self.name, "play": self.is_playing})

    def increase_small(self):
        self.set_timestamp(self.timestamp + self.step_size_small, source=self.name)

    def decrease_small(self):
        self.set_timestamp(self.timestamp - self.step_size_small, source=self.name)

    def play_pressed(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.btn_play.setText("Pause")
            self.timer.start()
        else:
            self.btn_play.setText("Play")
            self.timer.stop()
        self.publish_play_status()

    def on_play_update(self):
        self.increase_small()

    def increase_large(self):
        self.set_timestamp(self.timestamp + self.step_size_large, source=self.name)

    def decrease_large(self):
        self.set_timestamp(self.timestamp - self.step_size_large, source=self.name)
