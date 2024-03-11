import sys
import cv2
from pathlib import Path
import pickle
import numpy as np
from utils import make_image_grid


class ImageGridDisplay:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.xsize = 400
        self.ysize = 800
        self.current_index = 0

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

    def display_images(self):
        while True:
            chunk = self.chunks[self.current_index]
            images = [np.vstack([x[0][0]["crop"], x[1][0]["crop"]]) for x in chunk]
            grid = make_image_grid(images)
            cv2.imshow("imgrid", grid)
            k = cv2.waitKey(0)
            if k == ord("q"):
                break
            if k == ord("l"):
                self.current_index += 1
            if k == ord("h"):
                self.current_index -= 1
        cv2.destroyAllWindows()


# Example usage:
model_directory = Path("/data/proposed")
image_grid_display = ImageGridDisplay(model_directory)
image_grid_display.display_images()
