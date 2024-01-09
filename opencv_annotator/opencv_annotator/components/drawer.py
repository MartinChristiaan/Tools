# %%

import cv2
import numpy as np
from loguru import logger
from opencv_annotator.state import Observable, State


class Drawer:
    def __init__(
        self,
        state: State,
        line_thickness=2,
    ) -> None:
        self.line_thickness = line_thickness
        self.state = state
        self.output_image = Observable(np.zeros((1, 1, 3), dtype=np.uint8))
        state.detections_zoomed.subscribe(self.update, True)
        state.texted_image.subscribe(self.update, True)
        self.prev_zoom = state.zoom.value
        self.initialized = False
        self.draw_labels = True
        self.state.keyboard_event.subscribe(self.keyboard_callback)

    def write_bbox(self, image, detection, color, label=None):
        x = int(detection.bbox_x)
        y = int(detection.bbox_y)
        w = int(detection.bbox_w)
        h = int(detection.bbox_h)
        x2 = x + w
        y2 = y + h

        new_image = cv2.rectangle(image, (x, y), (x2, y2), color, self.line_thickness)

        if label is not None and self.draw_labels:
            tf = max(self.line_thickness - 1, 1)  # font thickness
            t_size = cv2.getTextSize(
                label, 0, fontScale=self.line_thickness / 3, thickness=tf
            )[0]
            c2 = x + t_size[0], y - t_size[1] - 3
            cv2.rectangle(new_image, (x, y), c2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(
                new_image,
                label,
                (x, y - 2),
                0,
                self.line_thickness / 3,
                [225, 255, 255],
                thickness=tf,
                lineType=cv2.LINE_AA,
            )

        return new_image

    def update(self):
        if not self.initialized:
            print(" returning det")
            self.initialized = True
            # needed to avoid double exec
            return

        if self.state.zoom.value == self.prev_zoom:
            # copy in case of new detection
            # logger.debug("copying")
            img = self.state.texted_image.value.copy()
        else:
            # logger.debug(f"{self.prev_zoom} {self.state.zoom.value}")
            img = self.state.texted_image.value
            self.prev_zoom = self.state.zoom.value

        # logger.debug(f"added detection {len(self.state.detections.value)}")
        for annotation in self.state.detections_zoomed.value:
            color = annotation.get_color()
            img = self.write_bbox(img, annotation, color=color, label=annotation.label)
        self.state.detections_image.set_value(img)

    def keyboard_callback(self):
        self.state
        key = self.state.keyboard_event.value
        if key == "l":
            self.draw_labels = not self.draw_labels
            self.update()
