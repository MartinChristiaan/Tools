from dataclasses import dataclass
from typing import List
from enum import Enum

import pandas as pd


class AnnotationPostproc(Enum):
    NONE = 0
    STATIC = 1
    TRACK = 2


def index_to_postproc(index):
    if index == 1:
        return AnnotationPostproc.STATIC

    if index == 2:
        return AnnotationPostproc.TRACK
    return AnnotationPostproc.NONE


def postproc_to_index(postproc):
    if postproc == AnnotationPostproc.NONE:
        return 0

    if postproc == AnnotationPostproc.STATIC:
        return 1

    if postproc == AnnotationPostproc.TRACK:
        return 2


@dataclass
class Annotation:
    bbox_x: float
    bbox_y: float
    bbox_w: float
    bbox_h: float
    class_id: int
    label: str
    timestamp: float
    confidence: float = 2
    real_detection: float = 1
    track_id: int = 99
    n: int = 1
    postproc: AnnotationPostproc = AnnotationPostproc.NONE

    @property
    def upperleft(self):
        return self.bbox_x, self.bbox_y

    @property
    def downright(self):
        return self.bbox_x + self.bbox_w, self.bbox_y + self.bbox_h

    @staticmethod
    def from_pandas(df: pd.DataFrame):
        x = Annotation(0, 0, 0, 0, 0, "", 0)
        keys = set(x.__dict__.keys())
        dicts = df.to_dict(orient="records")

        return [
            Annotation(
                **{k: v for k, v in d.items() if k in keys and not k == "postproc"}
            )
            for d in dicts
        ]

    @staticmethod
    def to_pandas(annotations: List["Annotation"]):
        # dicts = df.to_dict(orient="records"
        return pd.DataFrame([x.__dict__ for x in annotations])

    @property
    def cx(self):
        return self.bbox_x + self.bbox_w / 2

    @property
    def cy(self):
        return self.bbox_y + self.bbox_h / 2

    def get_color(self):
        if self.real_detection == 0:
            return (255, 0, 0)  # blue
        if self.confidence < 0.22:
            return (0, 0, 255)
        if self.confidence < 0.35:
            return (0, 165, 255)
        return (0, 255, 0)

    @property
    def accepted(self):
        return self.confidence > 0.35

    def is_inside(self, x, y):
        return (
            self.bbox_x <= x <= self.bbox_x + self.bbox_w
            and self.bbox_y <= y <= self.bbox_y + self.bbox_h
        )
