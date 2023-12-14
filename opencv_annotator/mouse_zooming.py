from copy import deepcopy
from typing import List
import cv2
from annotation import Annotation


class Zoomer:
    def __init__(self, h, w) -> None:
        self.x_offset = 0
        self.y_offset = 0
        self.h = h
        self.w = w
        self.zoom = 1
        self.min_zoom = 1
        self.max_zoom = 5
        self.dirty = False
        self.new_height = h
        self.new_width = w

    def update_zoom(self, event, x, y, flags, param):
        # global base_img, zoom, min_zoom, max_zoom
        if event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                self.zoom *= 1.1
                self.zoom = min(self.zoom, self.max_zoom)
            else:
                self.zoom /= 1.1
                self.zoom = max(self.zoom, self.min_zoom)

            # img = base_img.copy()

            # Calculate zoomed-in image size
            self.new_width = round(self.w / self.zoom)
            self.new_height = round(self.h / self.zoom)

            # Calculate offset
            self.x_offset = round(x - (x / self.zoom))
            self.y_offset = round(y - (y / self.zoom))
            self.dirty = True
            # Crop image

    def update_detections(self, annotations: List[Annotation]):
        detections_out = []
        for base_annotation in annotations:
            annotation = deepcopy(base_annotation)
            annotation.bbox_x -= self.x_offset
            annotation.bbox_y -= self.y_offset
            annotation.bbox_x *= self.zoom
            annotation.bbox_y *= self.zoom
            annotation.bbox_w *= self.zoom
            annotation.bbox_h *= self.zoom
            detections_out.append(annotation)
        # detections_out.bbox.bbox[:, 3] *= self.zoom
        return detections_out

    def compensate_new_annotation(self, annotation: Annotation):
        annotation.bbox_x /= self.zoom
        annotation.bbox_y /= self.zoom
        annotation.bbox_w /= self.zoom
        annotation.bbox_h /= self.zoom
        annotation.bbox_x += self.x_offset
        annotation.bbox_y += self.y_offset

    def update_img(self, base_img):
        img = base_img.copy()
        img = img[
            self.y_offset : self.y_offset + self.new_height,
            self.x_offset : self.x_offset + self.new_width,
        ]
        img = cv2.resize(img, None, fx=self.zoom, fy=self.zoom)
        self.dirty = False
        return img
