import sys
import cv2
from pathlib import Path
import pickle
import numpy as np
import pandas as pd
from utils import make_image_grid

NUM_COLS = 6


class ImageGridDisplay:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.xsize = 400
        self.ysize = 800
        self.current_index = 0
        self.selected_crop_idx = 0
        self.mistakes_to_correct_idx = []
        self.mistakes_to_ignore_idx = []
        self.mouse_position = (0, 0)  # Initialize mouse position

        mistake_files = list(self.model_dir.rglob("*.pkl"))
        chunks = []
        for mfile in mistake_files:
            with open(mfile, "rb") as f:
                data = pickle.load(f)

            max_items_for_grid = 12
            chunks += [
                data[i : i + max_items_for_grid]
                for i in range(0, len(data), max_items_for_grid)
            ]
        self.chunks = chunks
        self.detections_to_change = []

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

        if event == cv2.EVENT_RBUTTONDOWN:
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
            chunk = self.chunks[self.current_index]
            images = [np.vstack([x[0][0]["crop"], x[1][0]["crop"]]) for x in chunk]
            types = [x[0][0]["mistake_type"] for x in chunk]

            grid = make_image_grid(
                images,
                types,
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
                    dtochange = self.chunks[self.selected_crop_idx][active_idx][0][0]
                    dtochange = {k: v for k, v in dtochange.items() if not k == "crop"}
                    self.detections_to_change.append(dtochange)

                for active_idx in self.mistakes_to_ignore_idx:
                    dtochange = self.chunks[self.selected_crop_idx][active_idx][0][0]
                    dtochange = {k: v for k, v in dtochange.items() if not k == "crop"}
                    dtochange["mistake_type"] == "ignore"
                    self.detections_to_change.append(dtochange)

                self.mistakes_to_correct_idx = []
                self.current_index += 1
                df = pd.DataFrame(self.detections_to_change)
                df.to_csv("detections_to_change.csv", index=False)
            #     self.current_index -= 1
        cv2.destroyAllWindows()


# Example usage:
model_directory = Path("/data/proposed")
image_grid_display = ImageGridDisplay(model_directory)
image_grid_display.display_images()
