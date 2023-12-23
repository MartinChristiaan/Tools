# %%
# %load_ext autoreload
# %autoreload 2
from dataclasses import dataclass
from math import inf

import cv2
import dlutils_ii as du
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import torch
from albumentations import LongestMaxSize, PadIfNeeded
from icecream import ic
from loguru import logger
from PIL import Image
from tqdm import tqdm


@dataclass
class TrackUpdateData:
    row_id: int
    track_id: int
    image: np.ndarray
    timestamp: float

    @staticmethod
    def build(row_id, row, frame):
        logger.debug(row)
        x, y, w, h = [int(row[f"bbox_{x}"]) for x in "xywh"]

        frame_crop = frame[y : y + h, x : x + w]

        if np.product(frame_crop.shape) == 0:
            return
        # track_images[track_id].append(frame_crop)
        return TrackUpdateData(row_id, row.track_id, frame_crop, row.timestamp)


class DetectionProvider:
    def __init__(
        self,
        pathfinder: du.Pathfinder,
        source="annotations",
        time_between_annotations=1,
        roi_size=256,
    ) -> None:
        # ANNOTATION_DATA = "annotation_data"
        # if ANNOTATION_DATA not in st.session_state:
        #     st.session_state[ANNOTATION_DATA] = pd.DataFrame()
        # self.annotations = pd.DataFrame
        self.pathfinder = pathfinder
        # TODO add sourcing
        if source == "annotations":
            self.annotations = pathfinder.media_manager.load_annotations()
        else:
            self.annotations = pathfinder.load_detections(
                pathfinder.media_manager, [source]
            )[0]
        self.dt = time_between_annotations
        self.max_imgs_per_batch = 120
        self.batched_annotations = self.get_batched_annotations()
        self.transforms = [
            LongestMaxSize(max_size=roi_size, always_apply=True),
            PadIfNeeded(
                min_height=roi_size,
                min_width=roi_size,
                always_apply=True,
                border_mode=cv2.BORDER_CONSTANT,
            ),
        ]

    def get_sparse_annotations(self):
        t_prev = -inf
        sparse_timestamps = []
        for t in self.annotations.timestamp.unique():
            if t > t_prev + self.dt:
                sparse_timestamps.append(t)
                t_prev = t
        return self.annotations[self.annotations.timestamp.isin(sparse_timestamps)]

    def get_batched_annotations(self):
        sparse_annotations = self.get_sparse_annotations()
        sparse_annotations["batch"] = [0] * len(sparse_annotations)
        prev_len = 0
        cur_batch = 0
        for track_id, track in sparse_annotations.groupby("track_id"):
            if prev_len + len(track) < self.max_imgs_per_batch or cur_batch == 0:
                prev_len += len(track)
            else:
                cur_batch += 1
                prev_len = len(track)
            sparse_annotations[sparse_annotations.track_id == track_id]["batch"] = [
                cur_batch
            ] * len(track)
        return sparse_annotations

    def get_images(self, batch_id):
        # frame = self.pathfinder.mm.get_frame_nearest(t)[0]
        # if len(track_images) + len(track) > max_imgs:
        # track_images[track_id] = []
        cur_tracks = self.batched_annotations[
            self.batched_annotations.batch == batch_id
        ]
        frame_lookup = {
            t: self.pathfinder.media_manager.get_frame_nearest(t)[0]
            for t in tqdm(cur_tracks.timestamp.unique())
        }
        data = []
        for i, row in cur_tracks.iterrows():
            frame = frame_lookup[row.timestamp]
            tudata = TrackUpdateData.build(i, row, frame)
            for t in self.transforms:
                tudata.image = t(image=tudata.image)["image"]
            if tudata is None:
                continue
            data.append(tudata)
        return data

    def get_rows(self, row_ids):
        return self.batched_annotations.loc[row_ids]


# %%
if __name__ == "__main__":
    from config import get_example_dataset_configs

    configs = get_example_dataset_configs()
    detection_provider = DetectionProvider(configs[0].pathfinder)
    out = detection_provider.get_images(0)
