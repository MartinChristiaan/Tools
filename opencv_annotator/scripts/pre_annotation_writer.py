from typing import List

import dlutils_ii as du
from dlutils_ii.dataset_cache.writer import LabelConfig
from dlutils_ii.dataset_config import DatasetConfig


class PreAnnotationWriter(du.Writer):
    def __init__(
        self,
        config: DatasetConfig,
        frame_offsets: List[int],
        labelconfig: LabelConfig = LabelConfig(),
        source="tyolov8/detections_tyolov8m-30112023.csv",
    ):
        self.source = source
        super().__init__(config, frame_offsets, labelconfig)

    def load_annotation_source(self):
        return self.pathfinder.media_manager.load(self.source)
