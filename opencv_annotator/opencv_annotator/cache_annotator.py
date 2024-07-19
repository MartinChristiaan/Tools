# %%
from copy import deepcopy
import os
import shutil
from typing import List

import cv2
import dlutils_ii as du
import numpy as np
import pandas as pd
from opencv_annotator.annotation import Annotation, AnnotationPostproc
from opencv_annotator.components.text_adder import TextRequest
from yolo_plugins.evaluation.mistake_analysis import vizualize_objects
from loguru import logger
from opencv_annotator.state import Observable, State


# %%


def apply_ignore_areas(annotations: List[Annotation]):
    ignore_areas = [x for x in annotations if x.label == "ignore_area"]
    if len(ignore_areas) == 0:
        return annotations
    other_annotations = [x for x in annotations if x.label != "ignore_area"]
    filtered_annotations = []
    for a in other_annotations:
        ignored = False
        for ignore_area in ignore_areas:
            if ignore_area.is_inside(a.cx, a.cy):
                ignored = True
        if not ignored:
            filtered_annotations.append(a)

    num_filtered_annotations = len(annotations) - len(filtered_annotations)
    logger.debug(f"filtered {num_filtered_annotations} annotations")
    return filtered_annotations + ignore_areas


class IOManager:
    def __init__(self, dataset_config: du.DatasetConfig, state: State) -> None:
        self.state = state
        self.pathfinder = dataset_config.pathfinder
        prediction_df = dataset_config.pathfinder.annotations().dropna()

        items = list(prediction_df.groupby("timestamp"))
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
        if key == "u":
            self.update_annotations()
        if key == "t":
            if self.tmp_annotation_path.exists():
                os.remove(self.tmp_annotation_path)
            self.current_annotations = pd.DataFrame()
            self.state.frame_index.set_value(0)
            self.frame_index = 0

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

    def update_annotations(self):
        config = self.dataset_config
        tmp_path = config.pathfinder.annotations_path.with_suffix(".tmp.csv")
        if tmp_path.exists():
            logger.info(f"saving {config.pathfinder.name}")
            annotations = pd.read_csv(tmp_path)
            annotations.drop(["track_id", "postproc"], axis="columns")
            config.pathfinder.media_manager.save_annotations(
                annotations, "smallObjectsCorrected", True
            )
            shutil.copy(self.tmp_annotation_path, config.pathfinder.annotations_path)
            os.remove(self.tmp_annotation_path)

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
        if self.frame_index + 1 < len(self.detections):
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
                x
                for x in annotations
                if x.track_id == 99 and x.postproc != AnnotationPostproc.NONE
            ]
            print([x.postproc for x in trackables])
            print(f"{len(trackables)} trackables")
            self.tracked_annotations = self.track(trackables)

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
        detections = apply_ignore_areas(detections)
        offset = self.dataset_config.options.offset_scales[0]
        print(offset)
        frames = [
            cv2.imread(self.dataset_config.pathfinder.frame_filename(o, timestamp))
            for o in [0, int(round(-15 * offset)), int(round(15 * offset))]
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
            if annotation.postproc == AnnotationPostproc.TRACK:
                tracker = cv2.TrackerKCF_create()
                tracker.init(frame0, bboxi)
                success, bbox = tracker.update(frame0)
                success, bbox = tracker.update(frame1)
            else:
                success = True
                bbox = bboxi
            if success and not annotation.postproc == AnnotationPostproc.NONE:
                new_annot = deepcopy(annotation)
                new_annot.timestamp = next_t
                new_annot.bbox_x = bbox[0]
                new_annot.bbox_y = bbox[1]
                new_annot.bbox_w = bbox[2]
                new_annot.bbox_h = bbox[3]
                tracked.append(new_annot)
        return tracked
