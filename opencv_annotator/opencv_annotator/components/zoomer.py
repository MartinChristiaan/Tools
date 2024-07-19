from copy import deepcopy

import cv2
import numpy as np
from opencv_annotator.annotation import Annotation
from loguru import logger
from numpy import ndarray
from opencv_annotator.state import Observable, State

# Always execute worstcase = best? Zoom -> draw overlay  -> Draw detections, never copy


class Zoomer:
    def __init__(self, state: State) -> None:
        self.state = state
        # self.zoom = Observable(1)

        # self.zoomed_image = Observable(self.input_image.value)

        self.x_offset = 0
        self.y_offset = 0
        self.min_zoom = 1
        self.max_zoom = 8
        self.new_height = 1080
        self.new_width = 1920
        self.scale = 1
        # # self.raw_detections = raw_detections
        # self.raw_detections.subscribe(self.update_detections)
        state.base_image.subscribe(self.update_img)
        state.detections.subscribe(self.update_detections)
        state.mouse_event.subscribe(self.mouse_callback)
        state.zoom.subscribe(self.update_detections)
        state.zoom.subscribe(self.update_img)
        state.keyboard_event.subscribe(self.keyboard_callback)
        super().__init__()

    def mouse_callback(self):
        state = self.state
        zoom = state.zoom.value
        mouse_state = state.mouse_event.value
        x = mouse_state.x
        y = mouse_state.y
        if mouse_state.event == cv2.EVENT_MOUSEWHEEL:
            if mouse_state.flags > 0:
                zoom *= 1.1
                zoom = min(zoom, self.max_zoom)
            else:
                zoom /= 1.1
                zoom = max(zoom, self.min_zoom)

            self.new_width = round(self.w / zoom)
            self.new_height = round(self.h / zoom)

            # self.dirty = True
            state.zoom.set_value(zoom)

            self.x_offset = round(x / self.scale - (x / self.scale / zoom))
            self.y_offset = round(y / self.scale - (y / self.scale / zoom))
            # logger.debug("scrolling")

    def keyboard_callback(self):
        state = self.state
        key = state.keyboard_event.value
        zoom = state.zoom.value
        mouse_state = state.mouse_event.value
        x = mouse_state.x
        y = mouse_state.y
        if key in "ws":
            if key == "w":
                zoom *= 2
                zoom = min(zoom, self.max_zoom)
            else:
                zoom /= 2
                zoom = max(zoom, self.min_zoom)

            self.new_width = round(self.w / zoom)
            self.new_height = round(self.h / zoom)

            # self.dirty = True
            state.zoom.set_value(zoom)

            self.x_offset = round(x / self.scale - (x / self.scale / zoom))
            self.y_offset = round(y / self.scale - (y / self.scale / zoom))

    def update_detections(self):
        zoom = self.state.zoom.value
        detections_out = []
        for base_annotation in self.state.detections.value:
            annotation = deepcopy(base_annotation)
            annotation.bbox_x -= self.x_offset
            annotation.bbox_y -= self.y_offset
            annotation.bbox_x *= zoom * self.scale
            annotation.bbox_y *= zoom * self.scale
            annotation.bbox_w *= zoom * self.scale
            annotation.bbox_h *= zoom * self.scale
            detections_out.append(annotation)
        self.state.detections_zoomed.set_value(detections_out)

    def compsensate_zoom(self, x, y):
        zoom = self.state.zoom.value
        x /= zoom * self.scale
        y /= zoom * self.scale
        # annotation.bbox_w /= self.zoom * self.scale
        # annotation.bbox_h /= self.zoom * self.scale
        x += self.x_offset
        y += self.y_offset
        return x, y

    def update_img(self):
        state = self.state
        img = state.base_image.value
        self.h, self.w = img.shape[:2]
        zoom = state.zoom.value
        img_out = img[
            self.y_offset : self.y_offset + self.new_height,
            self.x_offset : self.x_offset + self.new_width,
        ]
        if min(img_out.shape) == 0:
            logger.warning("shape 0 in zoom")
            return
        img_out = cv2.resize(img_out, None, fx=zoom * self.scale, fy=zoom * self.scale)
        state.zoomed_image.set_value(img_out)
