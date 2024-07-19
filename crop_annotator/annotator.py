import pickle
from pathlib import Path
from loguru import logger
import numpy as np

import cv2


labels = [
    "object",
    "person",
    "vehicle",
    "airborne_object",
    "bird",
    "drone",
    "aircraft",
    "helicopter",
    "ship",
    "animal",
]

COLUMNS = 22
CROP_SIZE = 128


def create_image_grid(crops, metadatas, columns=COLUMNS):
    rows = (len(crops) + columns - 1) // columns
    grid_width = columns * CROP_SIZE
    grid_height = rows * CROP_SIZE
    grid_image = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

    for i, (crop, metadata) in enumerate(zip(crops, metadatas)):
        x = (i % columns) * CROP_SIZE
        y = (i // columns) * CROP_SIZE
        label = metadata["label"]
        # pad crop so it is square
        h, w = crop.shape[:2]
        crop_padded = np.zeros((max(h, w), max(h, w), 3), dtype=np.uint8)
        crop_padded[:h, :w] = crop
        crop_resized = cv2.resize(crop, (CROP_SIZE, CROP_SIZE))
        crop_resized = cv2.putText(
            crop_resized,
            label,
            (10, crop_resized.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

        grid_image[y : y + CROP_SIZE, x : x + CROP_SIZE] = crop_resized
    return grid_image


def read_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def save_pickle(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)


class CropAnnotator:
    def __init__(self) -> None:
        self.current_label_index = 0
        self.clusters = list(Path("classification_crops_clustered").glob("*/*"))
        self.clusters.sort()
        self.cluster_idx = 0

    @property
    def current_label(self):
        return labels[self.current_label_index]

    def mouse_callback(self, event, x, y, flags, param):
        x_idx = (x - CROP_SIZE) // CROP_SIZE
        y_idx = y // CROP_SIZE
        idx = x_idx + y_idx * COLUMNS
        if event == cv2.EVENT_LBUTTONDOWN:
            self.metadatas[idx]["label"] = labels[self.current_label_index]
            logger.info(f"Labeling {idx} as {labels[self.current_label_index]}")

    def handle_key(self, key):
        # if digit key pressed, set current label index
        if key in [ord(str(i)) for i in range(10)]:
            self.current_label_index = key - ord("0")

    def run(self):
        cluster = self.clusters[self.cluster_idx]
        images = list(cluster.glob("*.jpg"))
        images.sort()
        meta_paths = [img.with_suffix(".pkl") for img in images]
        self.metadatas = [read_pickle(meta_path) for meta_path in meta_paths]
        images = [cv2.imread(str(image)) for image in images]
        while True:

            grid = create_image_grid(images, self.metadatas)
            sidebar = np.zeros((grid.shape[0], CROP_SIZE, 3), dtype=np.uint8)
            grid = np.hstack([sidebar, grid])
            for i, label in enumerate(labels):
                color = (
                    (255, 255, 255)
                    if i == self.current_label_index
                    else (128, 128, 128)
                )
                sidebar = cv2.putText(
                    grid,
                    label,
                    (10, 20 + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1,
                    cv2.LINE_AA,
                )

            cv2.imshow("Cluster", grid)
            cv2.setMouseCallback("Cluster", self.mouse_callback)
            k = cv2.waitKey(10)
            self.handle_key(k)
            if k == ord("q"):
                break
            if k == ord("d") or k == ord("a"):

                for p, m in zip(meta_paths, self.metadatas):
                    save_pickle(p, m)

                delta_idx = 1 if k == ord("d") else -1
                self.cluster_idx += delta_idx

                cluster = self.clusters[self.cluster_idx]
                images = list(cluster.glob("*.jpg"))
                images.sort()
                meta_paths = [img.with_suffix(".pkl") for img in images]
                self.metadatas = [read_pickle(path) for path in meta_paths]
                images = [cv2.imread(str(image)) for image in images]
            if k == ord("s"):
                for m in self.metadatas:
                    m["label"] = labels[self.current_label_index]

        cv2.destroyAllWindows()


annotator = CropAnnotator()
annotator.run()
