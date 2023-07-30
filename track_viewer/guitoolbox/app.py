import sys
from collections import defaultdict
from enum import Enum, auto
from typing import Union, List, Optional

from PySide6.QtWidgets import QApplication
from media_manager.core import MediaManager

from guitoolbox.models.base import VideoModel, TrackModel
from guitoolbox.models.media_manager import MediaManagerModel
from guitoolbox.models.tracker_toolbox import TrackerToolboxModel, DetectionsTrackerToolboxModel
from guitoolbox.panel import Panel
from guitoolbox.panels.button_bar import ButtonBarPanel
from guitoolbox.panels.track import TrackPanel
from guitoolbox.panels.video import VideoPanel
from guitoolbox.panels_gui import PanelsGUI
from guitoolbox.visualize import ColorMap
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks


class SyncMode(Enum):
    ALL = auto()
    VIDEO = auto()


class MainGUI:
    def __init__(
        self,
        videos: Union[Union[VideoModel, MediaManager], List[Union[VideoModel, MediaManager]]],
        tracks: Optional[Union[Union[TrackModel, Tracks], List[Union[TrackModel, Tracks]]]] = None,
        sync_mode: SyncMode = SyncMode.VIDEO,
    ):

        self.video_models = self.videos_as_models(videos)
        self.track_models = [] if tracks is None else self.tracks_as_models(tracks)
        self.sync_mode = sync_mode

        # Init application
        app = QApplication(sys.argv)

        # Create panels GUI
        panels_gui = PanelsGUI()

        panels = defaultdict(list)
        for idx, video_model in enumerate(self.video_models):
            panels_set = []

            if idx < len(self.track_models):
                tracks_model = self.track_models[idx]
                color_map = ColorMap(color_count=len(tracks_model))
            else:
                tracks_model = None
                color_map = ColorMap(color_count=10)

            video_view_panel = VideoPanel(video_model, tracks_model, color_map, name=f"VideoPanel{idx}")
            panels_gui.add_panel(video_view_panel, row=0, col=idx, title=video_view_panel.name, row_span=6)
            panels_set.append(video_view_panel)

            button_bar_panel = ButtonBarPanel(
                name=f"ButtonBarPanel{idx}",
                step_size_small=video_model.seconds_per_frame,
                step_size_large=video_model.seconds_per_frame * 100,
            )
            panels_gui.add_panel(button_bar_panel, row=6, col=idx, title=button_bar_panel.name)
            panels_set.append(button_bar_panel)
            panels_gui.button_bar_panel = button_bar_panel

            if tracks_model is not None:
                track_panel = TrackPanel(
                    tracks_model,
                    color_map,
                    name=f"TrackPanel{idx}",
                    timestamp_min=video_model.timestamps_first(),
                    timestamp_max=video_model.timestamps_last(),
                )
                panels_gui.add_panel(track_panel, row=7, col=idx, title=track_panel.name, row_span=6)
                panels_gui.track_view = track_panel.track_view
                panels_set.append(track_panel)

            if self.sync_mode == SyncMode.ALL:
                set_name = "link_all"
            elif self.sync_mode == SyncMode.VIDEO:
                set_name = f"video_{idx}"
            else:
                raise ValueError(self.sync_mode)
            panels[set_name].extend(panels_set)

        for panels_set in panels.values():
            self.link(panels_set)
        for panels_set in panels.values():
            for panel in panels_set:
                panel.setup()

        sys.exit(app.exec())

    def videos_as_models(
        self, videos: Union[Union[VideoModel, MediaManager], List[Union[VideoModel, MediaManager]]]
    ) -> List[VideoModel]:
        if not isinstance(videos, list):
            videos = [videos]
        video_models = []
        for video in videos:
            if isinstance(video, MediaManager):
                video = MediaManagerModel(media_manager=video)
            elif not isinstance(video, VideoModel):
                raise TypeError(
                    f"Videos should either be a subclass of VideoModel or be a MediaManager, but is: {type(video)}"
                )
            video_models.append(video)
        return video_models

    def tracks_as_models(
        self, tracks: Union[Union[TrackModel, Tracks], List[Union[TrackModel, Tracks]]]
    ) -> List[TrackModel]:
        if not isinstance(tracks, list):
            tracks = [tracks]
        track_models = []
        for track in tracks:
            if isinstance(track, Tracks):
                track = TrackerToolboxModel(track)
            elif isinstance(track, Detections):
                track = DetectionsTrackerToolboxModel(track)
            elif not isinstance(track, TrackModel):
                raise TypeError(
                    f"Tracks should either be a subclass of TrackModel or be a Tracks, but is: {type(track)}"
                )
            track_models.append(track)
        return track_models

    # NOTE
    #  would be better if instead of List[Panel] something like List[TimeBasedPanel] was used which should contain the
    #  listen_to member function. However, subclassing of Panel twice crashes application, see also
    #  "example_interface_error.py"
    def link(self, panels: List[Panel]) -> None:
        panels_all = {panel.name for panel in panels}
        for panel in panels:
            panel.listen_to(panels_all)  # NOQA
