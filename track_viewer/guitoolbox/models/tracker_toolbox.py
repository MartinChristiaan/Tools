from guitoolbox.models.base import TrackModel
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks
from datetime import datetime


class TrackerToolboxModel(TrackModel):
    def __init__(self, tracks: Tracks):
        tracks = tracks.to_pandas()
        tracks["center_y"] = tracks["bbox_y"]
        tracks["center_x"] = tracks["bbox_x"] + (tracks["bbox_w"] / 2)
        tracks["datetime"] = [datetime.utcfromtimestamp(x) for x in tracks['timestamp']]
        super().__init__(tracks)


class DetectionsTrackerToolboxModel(TrackModel):
    def __init__(self, detections: Detections):
        detections = detections.to_pandas()
        detections["center_y"] = detections["bbox_y"]
        detections["center_x"] = detections["bbox_x"] + (detections["bbox_w"] / 2)
        # Track IDs are currently a requirement. As we only have detections, just assign a unique track ID to each item
        detections["track_id"] = list(range(len(detections)))
        super().__init__(detections)
