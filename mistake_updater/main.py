from datetime import datetime

# %%
from dataclasses import dataclass
import sys
from typing import List
import cv2
from pathlib import Path
import pickle
import numpy as np
import pandas as pd

from utils import make_image_grid

NUM_COLS = 6


@dataclass
class Mistakes:
    videoset: str
    camera: str
    image_crops: List[np.ndarray]
    detections: pd.DataFrame
    annotations_suffix: str


class ImageGridDisplay:
    def __init__(self, mistake_file: Path):
        # self.model_dir = model_dir
        self.xsize = 400
        self.ysize = 800
        self.current_index = 0
        self.selected_crop_idx = 0
        self.mistakes_to_correct_idx = []
        self.mistakes_to_ignore_idx = []
        self.mouse_position = (0, 0)  # Initialize mouse position

        # mistake_files = list(self.model_dir.rglob("*.pkl"))
        # chunks = []
        data = []
        # for mfile in mistake_files:
        with open(mistake_file, "rb") as f:
            data = pickle.load(f)
        self.data = data
        crops = data["image_crops"]
        detections = data["detections"]
        max_items_for_grid = 12
        chunks = [
            (
                crops[i : i + max_items_for_grid],
                detections.iloc[i : i + max_items_for_grid],
            )
            for i in range(0, len(crops), max_items_for_grid)
        ]
        self.chunks = chunks
        self.detections_to_change = []
        self.mistake_file = mistake_file

    def get_1d_idx(self, x, y):

        idx_x = x // self.xsize
        idx_y = y // self.ysize
        return idx_y * NUM_COLS + idx_x

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            self.mouse_position = (x, y)
            self.selected_crop_idx = self.get_1d_idx(x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            idx_to_toggle = self.get_1d_idx(x, y)
            if idx_to_toggle in self.mistakes_to_correct_idx:
                self.mistakes_to_correct_idx.remove(idx_to_toggle)
            else:
                self.mistakes_to_correct_idx.append(idx_to_toggle)

        if event == cv2.EVENT_LBUTTONDBLCLK:
            idx_to_toggle = self.get_1d_idx(x, y)
            if idx_to_toggle in self.mistakes_to_correct_idx:
                self.mistakes_to_ignore_idx.remove(idx_to_toggle)
            else:
                self.mistakes_to_ignore_idx.append(idx_to_toggle)

    def display_images(self):
        cv2.namedWindow("imgrid")
        cv2.setMouseCallback("imgrid", self.on_mouse)

        while True:
            if self.current_index >= len(self.chunks):
                break
            images, detections = self.chunks[self.current_index]
            grid = make_image_grid(
                images,
                list(detections.mistake_type),
                selected_idx=self.selected_crop_idx,
                active_idx=self.mistakes_to_correct_idx,
                ignore_idx=self.mistakes_to_ignore_idx,
            )
            cv2.imshow("imgrid", grid)
            k = cv2.waitKey(5)

            if k == ord("q"):
                break
            if k == ord("d"):
                for active_idx in self.mistakes_to_correct_idx:
                    self.detections_to_change.append(detections.iloc[active_idx])

                for active_idx in self.mistakes_to_ignore_idx:
                    dtochange = detections.iloc[active_idx]
                    dtochange["mistake_type"] == "ignore"
                    # self.detections_to_change.append(dtochange)
                    self.detections_to_change.append(dtochange)
                self.mistakes_to_correct_idx = []
                self.current_index += 1
                df = pd.DataFrame(self.detections_to_change)
                df.to_csv("detections_to_change.csv", index=False)
            #     self.current_index -= 1
        cv2.destroyAllWindows()
        df = pd.DataFrame(self.detections_to_change)
        resolvable = dict(
            videoset=self.data["videoset"],
            camera=self.data["camera"],
            annotation_suffix=self.data["annotations_suffix"],
            detections=df,
        )
        new_path = self.mistake_file.parent / self.mistake_file.stem.replace(
            "mistakes", "corrections.pkl"
        )
        with open(new_path, "wb") as f:
            pickle.dump(resolvable, f)


index = 11
# Example usage:
if __name__ == "__main__":
    model_directory = Path("/data/proposed")
    mistake_files = list(model_directory.rglob("*_mistakes.pkl"))
    mistake_files.sort()
    mfile = mistake_files[index]
    print(mfile)
    output_file = mistake_files[index]
    image_grid_display = ImageGridDisplay(mfile)
    image_grid_display.display_images()
