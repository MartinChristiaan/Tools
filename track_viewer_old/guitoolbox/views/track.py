from typing import Callable

import pandas as pd
import seaborn as sns
from guitoolbox.models.base import TrackModel
from guitoolbox.visualize import ColorMap
from matplotlib.backend_bases import PickEvent
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


class TrackView(FigureCanvasQTAgg):
    def __init__(
        self,
        timestamp_min: float,
        timestamp_max: float,
        tracks_model: TrackModel,
        color_map: ColorMap,
        on_timestamp_changed: Callable,
        width: int = 10,
        height: int = 8,
        dpi: int = 100,
        label_x: str = "timestamp",
        label_y: str = "center_x",
    ):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

        self.tracks_model = tracks_model
        self.color_map = color_map
        self.on_timestamp_changed = on_timestamp_changed

        self.timestamp = 0.0
        self.timestamp_min = min(timestamp_min, self.tracks_model.timestamps_first())
        self.timestamp_max = max(timestamp_max, self.tracks_model.timestamps_last())

        self.label_x = label_x
        self.label_y = label_y

        self.color_by = "track_id"
        self.color_constant = (1.0, 0.0, 0.0)

        self.slider_color = "r"
        self.slider = None

        # Controls which portion of the tracks is visible, i.e. is zoomed in to
        self.zoom = 1
        self.zoom_factor = 2
        self.view_window_margin = 1
        self.mpl_connect("scroll_event", self.scroll_figure)

        self.mpl_connect("button_press_event", self.button_press_figure)
        self.mpl_connect("pick_event", self.on_pick)

        # Setup context menu
        # See: https://www.pythonguis.com/tutorials/pyside6-signals-slots-events/
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        self.plot_xt_efficiently(picker=True, pickradius=1)

    def toggle_ylabel(self):
        if self.label_y == "center_x":
            self.label_y = "center_y"
        else:
            self.label_y = "center_y"
        print("changed ylabel")
        self.plot_xt_efficiently(picker=True, pickradius=1)
        self.render()

    def on_pick(self, event: PickEvent):
        if event.mouseevent.button == 1 and isinstance(event.artist, Line2D):
            track_id = event.artist.track_id
            print(self.tracks_model.tracks_by_id.get_group(track_id))
        elif not isinstance(event.artist, Line2D):
            print("Picked object which is not a Line2D")

    def button_press_figure(self, event):
        """Clicking the middle mouse button resets the zoom level"""
        if event.button == 1:
            # Left button
            if event.xdata is not None:
                self.frame_timestamp_set_value(event.xdata)
        elif event.button == 2:
            self.zoom_reset()  # Middle button
        elif event.button == 3:
            pass  # Right button
        else:
            assert False, "Unknown button"

    def frame_timestamp_set_value(self, timestamp: float):
        self.on_timestamp_changed(timestamp)

    def plot_xt_efficiently(self, **kwargs):
        # Clean axes, required for subsequent calls to this function
        # TODO use: https://stackoverflow.com/a/40139416/8488985

        self.axes_clear()
        self.axes.grid(1)
        # Plot either:
        #   - Lines if a track has at least 2 points, or
        #   - Points if a track has only 1 point
        # See: https://stackoverflow.com/a/43220120/8488985
        lines_xy, line_colors = [], []
        points_x, points_y, points_color = [], [], []
        track_ids = []
        for track_id, detections in self.tracks_model.tracks_by_id:
            xx = detections[self.label_x]
            yy = detections[self.label_y]
            color = self.color_map[track_id]  # NOQA
            colors = color
            if len(xx) == 1:
                points_x.extend(xx)
                points_y.extend(yy)
                points_color.append(color)
            else:
                lines_xy.append(xx)
                lines_xy.append(yy)
                line_colors.append(colors)
            track_ids.append(detections.track_id.unique().item())
        l = self.axes.plot(
            *lines_xy,
            **kwargs,
        )
        p = self.axes.scatter(points_x, points_y, c=points_color)
        for line, c in zip(l, line_colors):
            line.set_color(c)
        self.axes.set_xlabel(self.label_x)
        self.axes.set_ylabel(self.label_y)
        sns.despine(ax=self.axes)
        # TODO do for "p" (pathcollection) the same as is done here for "l".
        for track_id, x in zip(track_ids, l):
            x.track_id = track_id

    def axes_clear(self):
        self.axes.cla()
        self.slider = None

    def set_timestamp(self, timestamp: float):
        self.timestamp = timestamp
        self.render()

    def update_slider(self):
        if self.slider is None:
            self.slider = self.axes.axvline(x=self.timestamp, color=self.slider_color)
        else:
            self.slider.set_xdata([self.timestamp])

    def render(self):
        self.update_slider()
        self.update_view_window()
        self.draw()

    def scroll_figure(self, mouse_event):
        """Scrolling up in figure increases the zoom level, vice versa for scrolling down"""
        if mouse_event.button == "up":
            self.zoom_in()
        else:
            self.zoom_out()

    def zoom_out(self):
        self.zoom = max(self.zoom / self.zoom_factor, 1)
        self.render()

    def zoom_in(self):
        self.zoom *= self.zoom_factor
        self.render()

    def zoom_reset(self):
        self.zoom = 1
        self.render()

    def update_view_window(self):
        # # Number of frames shown in the plot from the frame index towards the lower bound at a certain zoom level
        # # At zoom level 1 all frames are shown, at zoom level 2 half of the frames are shown, etc...
        # view_window_offset_x0 = floor((self.timestamp - self.timestamp_min) / self.zoom)
        # view_window_offset_x0 = max(view_window_offset_x0, self.timestamp_min)
        #
        # # Number of frames shown in the plot from the frame index towards the upper bound at a certain zoom level
        # # At zoom level 1 all frames are shown, at zoom level 2 half of the frames are shown, etc...
        # view_window_offset_x1 = ceil((self.timestamp_max - self.timestamp) / self.zoom)
        # view_window_offset_x1 = min(view_window_offset_x1, self.timestamp_max)
        #
        # x0_index = self.timestamp - view_window_offset_x0
        # x1_index = self.timestamp + view_window_offset_x1
        #
        # x0_timestamp = self.index_as_timestamp(x0_index) - self.view_window_margin
        # x1_timestamp = self.index_as_timestamp(x1_index) + self.view_window_margin
        #
        # self.axes.set_xlim([x0_timestamp, x1_timestamp])

        a = (
            max(
                (self.timestamp_max - self.timestamp),
                (self.timestamp - self.timestamp_min),
            )
            / self.zoom
        )

        x0_timestamp = (
            max(self.timestamp_min, self.timestamp - a) - self.view_window_margin
        )
        x1_timestamp = (
            min(self.timestamp_max, self.timestamp + a) + self.view_window_margin
        )

        self.axes.set_xlim([x0_timestamp, x1_timestamp])

    def on_context_menu(self, pos):
        context = QMenu(self)

        # Zoom in with 'z'
        action = QAction("Zoom in", self)
        action.triggered.connect(self.zoom_in)  # NOQA
        context.addAction(action)

        # Zoom out with 'x'
        action = QAction("Zoom out", self)
        action.triggered.connect(self.zoom_out)  # NOQA
        context.addAction(action)

        # Zoom reset with 'c'
        action = QAction("Zoom reset", self)
        action.triggered.connect(self.zoom_reset)  # NOQA
        context.addAction(action)

        # Switch label on y-axis with 'l'
        action = QAction("Switch y-axis label", self)
        action.triggered.connect(self.label_y_axis_switch)  # NOQA

        context.exec_(self.mapToGlobal(pos))

    def label_y_axis_switch(self):
        if self.label_y == "center_x":
            self.label_y = "center_y"
        elif self.label_y == "center_y":
            self.label_y = "center_x"
        else:
            assert False, f"Unkown/Invalid label to switch {self.label_y}"
        print(f"New y label: {self.label_y}")
        self.plot_xt_efficiently(picker=True, pickradius=1)
        self.render()
