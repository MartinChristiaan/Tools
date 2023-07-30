from typing import Sequence, Optional

import numpy as np
import pandas as pd


class VideoModel:
    def __init__(self, timestamps: Sequence[float]):
        self._timestamps = timestamps
        self.seconds_per_frame = np.min(np.diff(self._timestamps))

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, timestamp: float):
        if not isinstance(timestamp, float):
            raise TypeError(f"timestamp: {timestamp} should be a float, but is {type(timestamp)}")

    def timestamps_first(self):
        return self._timestamps[0]

    def timestamps_last(self):
        return self._timestamps[-1]

    def __contains__(self, timestamp: float):
        return self.timestamps_first() <= timestamp <= self.timestamps_last()


class TrackModel:
    def __init__(self, tracks: pd.DataFrame):
        self.tracks = tracks
        self.tracks_by_id = tracks.groupby("track_id")
        self._tracks_by_timestamp = tracks.groupby("timestamp")
        self._timestamps = sorted(self._tracks_by_timestamp.groups.keys())  # NOQA

    def __len__(self):
        return len(self.tracks_by_id)

    def track_ids(self):
        return self.tracks_by_id.groups

    def detections_by_timestamp(self, timestamp: float) -> Optional[pd.DataFrame]:
        try:
            detections = self._tracks_by_timestamp.get_group(timestamp)  # self._tracks_by_timestamp.groups
        except KeyError:
            detections = None
        return detections

    def timestamps_first(self) -> float:
        return self._timestamps[0]  # NOQA

    def timestamps_last(self) -> float:
        return self._timestamps[-1]  # NOQA

    def __contains__(self, timestamp: float):
        return self._timestamps

