import os
from typing import List

import dlutils_ii as du
from dlutils_ii.dataset_cache.writer import LabelConfig
from dlutils_ii.dataset_config import DatasetConfig
import pandas as pd


def get_modified_date(path):
    return os.path.getmtime(path)


# Sort the list of Path objects by modified date


class PreAnnotationWriter(du.Writer):
    def __init__(
        self,
        config: DatasetConfig,
        frame_offsets: List[int],
        labelconfig: LabelConfig = LabelConfig(),
        # source="tyolov8/detections_tyolov8m-30112023.csv",
    ):
        super().__init__(config, frame_offsets, labelconfig)

    def load_annotation_source(self):
        mm = self.pathfinder.media_manager
        paths = list(mm.result_dirpath.rglob("*.csv"))
        print(paths)
        sorted_paths = sorted(paths, key=get_modified_date)
        latest_path = [
            x for x in sorted_paths if "tyolov8" in str(x) and "track" in str(x)
        ]

        if len(latest_path) == 0:
            return None
        path = f"{latest_path[0].parent.stem}/{latest_path[0].name}"
        print(path)
        from_supra = "_supra" in path
        data = self.pathfinder.media_manager.load(
            path.replace("_supra/", ""), from_supra
        )
        print(data)
        return data


class MixedSourceWriter(du.Writer):
    def __init__(
        self,
        config: DatasetConfig,
        sources: List[str],
        frame_offsets: List[int],
        labelconfig: LabelConfig = LabelConfig(),
        # source="tyolov8/detections_tyolov8m-30112023.csv",
    ):
        self.sources = sources
        super().__init__(config, frame_offsets, labelconfig)

    def load_annotation_source(self):
        for source in self.sources:
            df = pd.read_csv(source)
            df["source"] = source

        return data
