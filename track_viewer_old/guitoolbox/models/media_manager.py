from typing import Tuple

import numpy as np
from guitoolbox.models.base import VideoModel
from media_manager.core import MediaManager


class MediaManagerModel(VideoModel):
    def __init__(self, media_manager: MediaManager):
        super().__init__(media_manager.timestamps)
        self.media_manager = media_manager

    def __len__(self):
        return len(self.media_manager)

    def __getitem__(self, item) -> Tuple[np.ndarray, float]:
        (
            media_index_video,
            file_index,
            timestamp_video,
            source_filepath,
            result_dirpath,
        ) = self.media_manager[item]
        frame = self.media_manager.get_frame(timestamp_video)
        return frame, timestamp_video
