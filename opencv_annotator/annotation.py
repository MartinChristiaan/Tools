from dataclasses import dataclass

import pandas as pd


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

    @property
    def upperleft(self):
        return self.bbox_x, self.bbox_y

    @property
    def downright(self):
        return self.bbox_x + self.bbox_w, self.bbox_y + self.bbox_h

    @staticmethod
    def from_pandas(df: pd.DataFrame):
        dicts = df.to_dict(orient="records")
        return [Annotation(**d) for d in dicts]

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
            return (0, 255, 255)
        return (0, 255, 0)
