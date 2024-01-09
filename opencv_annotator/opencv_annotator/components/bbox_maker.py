import cv2
import numpy as np
from opencv_annotator.annotation import Annotation, AnnotationPostproc
from opencv_annotator.cache_annotator import apply_ignore_areas
from opencv_annotator.components.zoomer import Zoomer
from opencv_annotator.state import Observable, State


class BBoxMaker:
    def __init__(
        self,
        state: State,
        zoomer: Zoomer
        # timestamp,
        # im_width,
        # detections: Observable[List[Annotation]],
        # zoomer: Zoomer,
        # mouse_state: Observable[MouseState],
        # selected_class: Observable[str],
    ) -> None:
        # self.zoom = zoomer.zoom
        self.zoomer = zoomer
        self.new_annotation = None
        self.is_button_down = False
        self.new_annotation_ready = False
        self.state = state
        # self.im_width = im_width
        # self.mouse_state = mouse_state
        state.mouse_event.subscribe(self.mouse_callback)
        state.keyboard_event.subscribe(self.keyboard_callback)
        # self.detections = detections
        # self.selected_class = selected_class
        self.annotation_centers = []
        super().__init__()

    def mouse_callback(self):
        detections = self.state.detections
        m = self.state.mouse_event.value
        x, y = self.zoomer.compsensate_zoom(m.x, m.y)
        if m.x > self.state.base_image.value.shape[1]:
            return

        if m.event == cv2.EVENT_MOUSEMOVE and self.is_button_down:
            self.new_annotation.bbox_w = x - self.new_annotation.bbox_x
            self.new_annotation.bbox_h = y - self.new_annotation.bbox_y
            detections.set_value(detections.value)

        elif m.event == cv2.EVENT_RBUTTONDOWN:
            for a in detections.value:
                if a.is_inside(x, y):
                    detections.value.remove(a)
                    detections.set_value(detections.value)
                    self.state.zoom.set_value(self.state.zoom.value)
                    return

        elif m.event == cv2.EVENT_LBUTTONDOWN:
            for a in detections.value:
                if a.is_inside(x, y):
                    a.confidence = 1
                    a.label = self.state.current_class.value
                    a.real_detection = True
                    detections.set_value(detections.value)
                    return

            self.new_annotation = Annotation(
                x,
                y,
                1,
                1,
                0,
                self.state.current_class.value,
                self.state.timestamp.value,
                postproc=self.state.postproc_index.value,
            )
            new_detections = detections.value + [self.new_annotation]

            detections.set_value(new_detections)
            self.is_button_down = True
            # if inside annotation -> confirm

        elif m.event == cv2.EVENT_LBUTTONUP:
            if not self.is_button_down:
                return
            if self.new_annotation.bbox_w < 0:
                self.new_annotation.bbox_x += self.new_annotation.bbox_w
                self.new_annotation.bbox_w *= -1

            if self.new_annotation.bbox_h < 0:
                self.new_annotation.bbox_y += self.new_annotation.bbox_h
                self.new_annotation.bbox_h *= -1
            new_detections = detections.value
            # print("new_detections", new_detections)
            if self.state.current_class.value == "ignore_area":
                new_detections = apply_ignore_areas(new_detections)
            self.is_button_down = False
            detections.set_value(new_detections)

    def keyboard_callback(self):
        state = self.state
        key = state.keyboard_event.value
        if key == "i":
            state.detections.set_value(
                [Annotation(0, 0, 500, 500, 10, "ignore_frame", state.timestamp.value)]
            )

            state.keyboard_event.set_value("d")
        elif key == "r":
            state.detections.set_value(
                [x for x in state.detections.value if x.real_detection]
            )
