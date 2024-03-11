import sys
import cv2
from pathlib import Path
import pickle
import numpy as np
from utils import make_image_grid

NUM_COLS = 6


class ImageGridDisplay:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.xsize = 400
        self.ysize = 800
        self.current_index = 0
        self.selected_crop_idx = 0
        self.active_crop_idx = []
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

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            self.mouse_position = (x, y)
            idx_x = x // self.xsize
            idx_y = y // self.ysize
            self.selected_crop_idx = idx_y * NUM_COLS + idx_x
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_position = (x, y)
            idx_x = x // self.xsize
            idx_y = y // self.ysize
            idx_to_toggle = idx_y * NUM_COLS + idx_x
            if idx_to_toggle in self.active_crop_idx:
                self.active_crop_idx.remove(idx_to_toggle)
            else:
                self.active_crop_idx.append(idx_to_toggle)

    def display_images(self):
        cv2.namedWindow("imgrid")
        cv2.setMouseCallback("imgrid", self.on_mouse)

        while True:
            if self.current_index >= len(self.chunks):
                break
            chunk = self.chunks[self.current_index]
            images = [np.vstack([x[0][0]["crop"], x[1][0]["crop"]]) for x in chunk]

            grid = make_image_grid(
                images,
                selected_idx=self.selected_crop_idx,
                active_idx=self.active_crop_idx,
            )
            cv2.imshow("imgrid", grid)
            k = cv2.waitKey(20)
            if k == ord("q"):
                break
            if k == ord("l"):
                for x in self.active_crop_idx:
                    dtochange = self.chunks[x][0][0]
                    print(dtochange)
                    del dtochange["crop"]
                    self.detections_to_change.append(dtochange)
                self.active_crop_idx = []
                self.current_index += 1
            #     self.current_index -= 1
        cv2.destroyAllWindows()


# Example usage:
model_directory = Path("/data/proposed")
image_grid_display = ImageGridDisplay(model_directory)
image_grid_display.display_images()
