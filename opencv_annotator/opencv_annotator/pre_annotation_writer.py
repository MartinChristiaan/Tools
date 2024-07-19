import fnmatch
import os
from typing import List

import dlutils_ii as du
from dlutils_ii.dataset_cache.writer import LabelConfig
from dlutils_ii.dataset_config import DatasetConfig
from loguru import logger
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
    # Problem, you may want to prioritize annotations and then detections from another
    def __init__(
        self,
        config: DatasetConfig,
        source_glob_pattern: str,
        frame_offsets: List[int],
        labelconfig: LabelConfig = LabelConfig(),
        # source="tyolov8/detections_tyolov8m-30112023.csv",
    ):
        self.source_glob_pattern = source_glob_pattern
        super().__init__(config, frame_offsets, labelconfig)

    def load_annotation_source(self):
        """
        #TODO run testing for various examples... should download a videoset
        """
        data = []
        mm = self.pathfinder.media_manager
        paths = list(map(str, mm.result_dirpath.rglob("*.csv")))
        filtered_paths = []
        for pattern in self.source_glob_pattern.split("+"):
            filtered_paths += fnmatch.filter(paths, pattern)
        paths = list(set(filtered_paths))
        for path in paths:
            print(path)
            df = pd.read_csv(path)
            name = str(path).replace(str(mm.result_dirpath), "")
            df["source"] = [name] * len(df)
            if not "confidence" in df.columns:
                df["confidence"] = [1] * len(df)
            data.append(df)

        if len(data) == 0:
            logger.error(f"no data found for {self.pathfinder.name}")
            return None
        df = pd.concat(data)
        annotation_timestamps = []
        other_timestamps = []
        for i, row in df.iterrows():
            if "_annotatations" in row["source"]:
                annotation_timestamps.append(row.timestamp)
            else:
                other_timestamps.append(row.timestamp)

        max_other_samples = self.train_options.max_samples - len(annotation_timestamps)
        annotation_timestamps = self.limit_exported_samples(annotation_timestamps)
        other_timestamps = self.limit_exported_samples(
            other_timestamps, max_other_samples
        )
        final_df = df[df.timestamp.isin(annotation_timestamps + other_timestamps)]
        return final_df
