# %%
from copy import deepcopy
from typing import List

import cv2
import dlutils_ii as du
import numpy as np
import pandas as pd
from annotation import Annotation
from components.text_adder import TextRequest
from dlutils_ii.annotation_cache.writer_annotations import vizualize_objects
from loguru import logger
from state import Observable, State

# %%


class IOManager:
    def __init__(self, dataset_config: du.DatasetConfig, state: State) -> None:
        self.state = state
        self.pathfinder = dataset_config.pathfinder
        items = list(dataset_config.pathfinder.annotations().groupby("timestamp"))
        self.timestamps = [x[0] for x in items]
        self.detections = [Annotation.from_pandas(x[1]) for x in items]

        self.dataset_config = dataset_config
        self.current_annotations = pd.DataFrame()
        if self.tmp_annotation_path.exists():
            self.current_annotations = pd.read_csv(self.tmp_annotation_path)
        self.state.timestamps.set_value(self.timestamps)
        self.frame_index = self.get_first_frame_index()
        self.tracked_annotations = []
        self.go_value = ""

        state.frame_index.subscribe(self.load_frame)
        state.keyboard_event.subscribe(self.keyboard_callback)

    def keyboard_callback(self):
        state = self.state
        key = state.keyboard_event.value
        frame_index = state.frame_index.value

        if key in "ad":
            self.save_tmp()
            if key == "a":
                frame_index -= 1
                if frame_index < 0:
                    frame_index = len(self.timestamps) - 1
            else:
                frame_index += 1
                if frame_index > len(self.timestamps) - 1:
                    frame_index = 0
            self.state.frame_index.set_value(frame_index)
            print("set new index")

        if state.keyboard_mode.value == "go":
            if key.isdigit():
                self.go_value += key
                state.zoom.run()
            else:
                try:
                    value = int(self.go_value)
                    state.frame_index.set_value(value)
                except:
                    print("failed")
                self.go_value = ""
                state.keyboard_mode.set_value("normal")

        if key == "g":
            state.keyboard_mode.set_value("go")
            state.zoom.run()

    def get_status(self):
        state = self.state
        if state.keyboard_mode.value == "go":
            return [
                TextRequest(
                    f"Frame selection : {self.go_value} ", (255, 255, 255), True
                )
            ]
        else:
            return [
                TextRequest(
                    f"Frame selection : {self.frame_index}/{len(self.timestamps)} (a-d)",
                    (255, 255, 255),
                    True,
                )
            ]

    @property
    def evaluated_timestamps(self):
        return self.current_annotations.timestamp.unique()

    def get_first_frame_index(self):
        if len(self.current_annotations) == 0:
            return 0
        for j in range(len(self.timestamps)):
            if self.timestamps[j] not in self.evaluated_timestamps:
                return j
        return 0

    @property
    def tmp_annotation_path(self):
        return self.pathfinder.annotations_path.with_suffix(".tmp.csv")

    def save_tmp(self):
        # get current annotations and put them in dataframe
        # ignore is put an ignore frame!
        annotations = self.state.detections.value
        if len(self.current_annotations) > 0:
            # avoid duplicates by removing previous
            self.current_annotations = self.current_annotations[
                ~(self.current_annotations.timestamp == self.state.timestamp.value)
            ]

        next_detections = self.detections[self.frame_index + 1]
        for x in annotations:
            if x.track_id == 99:
                continue
            next_item = [a for a in next_detections if a.track_id == x.track_id]
            if len(next_item) == 0:
                continue
            next_item[0].label = x.label
            # next_items.label = [x.label] * len(next_items)

        self.current_annotations = pd.concat(
            [self.current_annotations, Annotation.to_pandas(annotations)]
        )
        self.current_annotations.to_csv(self.tmp_annotation_path, index=False)
        self.tracked_annotations = []
        if self.should_track():
            trackables = [
                x for x in annotations if x.track_id == 99 and x.label != "ignore_frame"
            ]
            self.tracked_annotations = self.track(trackables)

    # def stop(self):
    #     return True

    def load_frame(self):
        self.frame_index = self.state.frame_index.value
        # timestamp, detections = self.items[self.frame_index]
        timestamp = self.timestamps[self.frame_index]
        detections = self.detections[self.frame_index]
        if (
            len(self.current_annotations)
            and timestamp in self.current_annotations.timestamp.unique()
        ):
            detections = Annotation.from_pandas(
                self.current_annotations[
                    self.current_annotations.timestamp == timestamp
                ]
            )
        detections += self.tracked_annotations
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
        self.state.timestamp.set_value(self.timestamps[self.frame_index])
        self.state.frame_inputs.set_value(self.frame_inputs)
        self.state.detections.set_value(detections)
        self.tracked_annotations = []
        print("set frame inputs")

    def should_track(self):
        # current_timestamp = self.items[self.frame_index][0]
        if len(self.timestamps) < self.frame_index + 2:
            return False
        next_timestamp = self.timestamps[self.frame_index + 1]
        return not next_timestamp in self.evaluated_timestamps

    def track(self, annotations: List[Annotation]):
        # TODO use other process for tracking. or as soon as bbox is drawn
        frame0 = self.frame_inputs["f0"]
        next_t = self.timestamps[self.frame_index + 1]
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
            tracker.init(frame0, bboxi)
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
