"""Shows how to quickly (and dirty) get an annotation tool from the track viewer"""
import os

from matplotlib.backend_bases import PickEvent
from matplotlib.lines import Line2D
from media_manager.core import MediaManager

from guitoolbox.app import MainGUI, SyncMode
from guitoolbox.views import track
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks


class AnnotationTrackView(track.TrackView):
    def on_pick(self, event: PickEvent):
        if event.mouseevent.button == 1 and isinstance(event.artist, Line2D):
            track_id = event.artist.track_id
            self.track_id_last = track_id

            # Use the env to keep track of data
            # First click on a track in the TrackViewer enters that ID in the env
            # Second click matches the two track IDs
            if "ANNOTATION_TRACK_ID" not in os.environ:
                print("first entry")
                os.environ["ANNOTATION_TRACK_ID"] = str(track_id)
            else:
                track_id0 = os.environ["ANNOTATION_TRACK_ID"]
                print(f"Matched track_id={track_id0} with track_id={track_id}")  # TODO do something, e.g. write to file
                del os.environ["ANNOTATION_TRACK_ID"]  # Reset

        elif not isinstance(event.artist, Line2D):
            print("Picked object which is not a Line2D")


# HACK monkey patch class
track.TrackView = AnnotationTrackView

dirname = r"\\diskstationii1\spear\data\Recordings\20230413_avalor_simulation"
mm0 = MediaManager(
    os.path.join(dirname, r"video\EO"),
    result_dirpath=os.path.join(dirname, r"\results\EO"),
    video_suffix=".avi",
    log_column_to_use=1,
)

mm1 = MediaManager(
    os.path.join(dirname, r"video\EO"),
    result_dirpath=os.path.join(dirname, r"\results\EO"),
    video_suffix=".avi",
    log_column_to_use=1,
)

tracks = Tracks.load(os.path.join(dirname, r"results\tracks\tracks_EO_live.csv"))
detections = Detections.load(os.path.join(dirname, r"results\detections\detections_EO_live.csv"))

# GUI
gui = MainGUI(
    videos=[mm0, mm1],
    tracks=[tracks, tracks],
    sync_mode=SyncMode.VIDEO,
)
