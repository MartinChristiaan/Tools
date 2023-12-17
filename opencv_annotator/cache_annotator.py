# %%
from copy import deepcopy
import sys
from typing import List
import cv2
from loguru import logger
import numpy as np
import pandas as pd
from annotation import Annotation
from annotator import BoundingBoxAnnotator, ReturnMode
from dlutils_ii.annotation_cache.writer_annotations import vizualize_objects
import dlutils_ii as du

# %%


class CacheAnnotator:
    def __init__(self, dataset_config: du.DatasetConfig) -> None:
        self.pathfinder = dataset_config.pathfinder
        self.items = list(dataset_config.pathfinder.annotations().groupby("timestamp"))
        self.action_lut = {
            ReturnMode.PREV: self.decrement_index,
            ReturnMode.NEXT: self.increment_index,
            ReturnMode.STOP: self.stop,
            # ReturnMode.SAVE: self.save_tmp,
        }
        self.dataset_config = dataset_config
        self.current_annotations = pd.DataFrame()
        if self.tmp_annotation_path.exists():
            self.current_annotations = pd.read_csv(self.tmp_annotation_path)
        self.annotator = BoundingBoxAnnotator()
        self.frame_index = self.get_first_frame_index()
        self.tracked_annotations = []

    def decrement_index(self):
        self.save_tmp()
        self.frame_index -= 1
        if self.frame_index < 0:
            self.frame_index = len(self.items) - 1

    def increment_index(self):
        self.save_tmp()
        self.frame_index += 1
        if self.frame_index > len(self.items) - 1:
            self.frame_index = 0

    @property
    def evaluated_timestamps(self):
        return self.current_annotations.timestamp.unique()

    def get_first_frame_index(self):
        if len(self.current_annotations) == 0:
            return 0
        timestamps = [x[0] for x in self.items]
        for j in range(len(timestamps)):
            if timestamps[j] not in self.evaluated_timestamps:
                return j
        return 0

    @property
    def tmp_annotation_path(self):
        return self.pathfinder.annotations_path.with_suffix(".tmp.csv")

    def save_tmp(self):
        # get current annotations and put them in dataframe
        # ignore is put an ignore frame!
        annotations = self.annotator.state.detections.value
        if len(self.current_annotations) > 0:
            # avoid duplicates by removing previous
            self.current_annotations = self.current_annotations[
                ~(
                    self.current_annotations.timestamp
                    == self.annotator.state.timestamp.value
                )
            ]

        self.current_annotations = pd.concat(
            [self.current_annotations, Annotation.to_pandas(annotations)]
        )
        self.current_annotations.to_csv(self.tmp_annotation_path, index=False)
        self.tracked_annotations = []
        if self.should_track():
            trackables = [x for x in annotations if x.label == "ignore_area"]
            self.tracked_annotations = self.track(trackables)

    def stop(self):
        return True

    def run(self):
        stop = False
        while not stop:
            timestamp, detections = self.items[self.frame_index]
            if (
                len(self.current_annotations)
                and timestamp in self.current_annotations.timestamp.unique()
            ):
                detections = self.current_annotations[
                    self.current_annotations.timestamp == timestamp
                ]
            detections = detections.sort_values(["bbox_y", "bbox_x"])
            detections = Annotation.from_pandas(detections) + self.tracked_annotations
            frames = [
                cv2.imread(self.dataset_config.pathfinder.frame_filename(o, timestamp))
                for o in [0, -15, 15]
            ]
            vizframe = vizualize_objects(frames)
            self.frame_inputs = {
                "motion_frame": vizframe,
                "f0": frames[0],
                "f15": frames[1],
                "f-15": frames[2],
            }
            print(vizframe.shape)
            result = self.annotator.run(self.frame_inputs, timestamp, detections)
            stop = self.action_lut[result]()

    def should_track(self):
        # current_timestamp = self.items[self.frame_index][0]
        if len(self.items) < self.frame_index + 2:
            return False
        next_timestamp = self.items[self.frame_index + 1][0]
        return not next_timestamp in self.evaluated_timestamps

    def track(self, annotations: List[Annotation]):
        # TODO use other process for tracking. or as soon as bbox is drawn
        frame0 = self.frame_inputs["f0"]
        next_t = self.items[self.frame_index + 1][0]
        frame1 = cv2.imread(self.dataset_config.pathfinder.frame_filename(0, next_t))
        # multi_tracker = cv2.MultiTracker_create()
        tracked = []
        logger.debug(f"tracking {len(annotations)} annotations")

        for annotation in annotations:
            bboxi = (
                int(annotation.bbox_x),
                int(annotation.bbox_y),
                int(annotation.bbox_w),
                int(annotation.bbox_h),
            )
            # multi_tracker.add(, frame0, bbox)
            tracker = cv2.TrackerKCF_create()
            ret = tracker.init(frame0, bboxi)
            success, bbox = tracker.update(frame0)
            success, bbox = tracker.update(frame1)
            if success:
                new_annot = deepcopy(annotation)
                new_annot.timestamp = next_t
                new_annot.bbox_x = bbox[0]
                new_annot.bbox_y = bbox[1]
                new_annot.bbox_w = bbox[2]
                new_annot.bbox_h = bbox[3]
                tracked.append(new_annot)
        return tracked
