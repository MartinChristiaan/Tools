import cv2
import numpy as np
from opencv_annotator.annotation import Annotation

# from opencv_annotator.state import ImageEditor
from opencv_annotator.components.zoomer import Zoomer
from opencv_annotator.state import MouseState, Observable, State


def split_list(input_list, n):
    """
    Split a list into n sublists.

    Parameters:
    - input_list (list): The input list to be split.
    - n (int): The number of sublists to create.

    Returns:
    - list of lists: A list containing n sublists.
    """
    if n <= 0:
        raise ValueError("Number of sublists (n) must be greater than 0.")

    # Calculate the length of each sublist
    sublist_length = len(input_list) // n
    remainder = len(input_list) % n

    # Create sublists
    sublists = [
        input_list[
            i * sublist_length
            + min(i, remainder) : (i + 1) * sublist_length
            + min(i + 1, remainder)
        ]
        for i in range(n)
    ]

    return sublists


class ROIManager:
    def __init__(
        self,
        zoomer: Zoomer,
        # detections: Observable[List[Annotation]],
        # mouse: Observable[MouseState],
        # raw_image: Observable[np.ndarray],
        # detections_img: Observable[np.ndarray],
        state: State,
    ) -> None:
        self.roi_size = 128
        self.upscale = 2
        self.num_cols = 3
        self.zoomer = zoomer
        state.mouse_event.subscribe(self.mouse_callback)
        # self.mouse = mouse
        # self.mouse.subscribe(self.mouse_callback)

        # self.detections = detections
        # self.raw_img = raw_image
        # self.detections_img = detections_img
        state.detections_image.subscribe(self.draw_rois)
        # self.out_image = Observable(detections_img.value)
        self.annotation_lut = {}
        self.state = state

    def mouse_callback(self):
        state = self.state
        m = state.mouse_event.value
        x = m.x
        y = m.y
        im_width = state.base_image.value.shape[1]
        event = m.event
        if x > im_width:
            xidx = (x - im_width) // self.roi_size
            yidx = y // self.roi_size
            if event == cv2.EVENT_LBUTTONDOWN:
                selected_annotation = self.annotation_lut[xidx][yidx]
                selected_annotation.confidence = 1
                selected_annotation.label = state.current_class.value
                selected_annotation.real_detection = True
                state.detections.set_value(state.detections.value)

            if event == cv2.EVENT_RBUTTONDOWN:
                new_dets = state.detections.value
                new_dets.remove(self.annotation_lut[xidx][yidx])
                state.detections.set_value(new_dets)

    def process_annotation(
        self, annotation: Annotation, frame: np.ndarray
    ) -> np.ndarray:
        x0 = annotation.cx - self.roi_size / 2 / self.upscale
        y0 = annotation.cy - self.roi_size / 2 / self.upscale
        x0 = int(np.clip(x0, 0, frame.shape[1] - self.roi_size / self.upscale - 1))
        y0 = int(np.clip(y0, 0, frame.shape[0] - self.roi_size / self.upscale - 1))

        roi = frame[
            y0 : y0 + self.roi_size // self.upscale,
            x0 : x0 + self.roi_size // self.upscale,
        ]
        roi = cv2.resize(roi, (self.roi_size, self.roi_size))
        bx0 = int((annotation.bbox_x - x0) * self.upscale)
        by0 = int((annotation.bbox_y - y0) * self.upscale)

        bx1 = int(bx0 + annotation.bbox_w * self.upscale)
        by1 = int(by0 + annotation.bbox_h * self.upscale)

        cv2.rectangle(roi, (bx0, by0), (bx1, by1), annotation.get_color(), 2)
        return roi

        #     self.dirty = True

        # Make it so that when the user hovers over one of the ROI's, its border will increase

    def draw_rois(self):
        state = self.state
        # state.get_runcounts()
        frame = state.detections_image.value
        h = frame.shape[0]
        if len(frame.shape) < 3:
            state.roi_image.set_value(state.detections_image)
            return
        max_rois = h // self.roi_size
        annotations = state.detections.value
        annotations_per_col = split_list(annotations, self.num_cols)
        rows = []
        for x_idx, annotations in enumerate(annotations_per_col):
            if len(annotations) == 0:
                continue
            rois = []
            for y_idx, annotation in enumerate(annotations[:max_rois]):
                roi = self.process_annotation(annotation, state.base_image.value)
                rois.append(roi)

            rois = np.vstack(rois)
            out_bar = np.zeros((h, self.roi_size, 3), dtype=np.uint8)
            out_bar[: rois.shape[0]] = rois
            rows.append(out_bar)
            self.annotation_lut[x_idx] = {
                y: annotation for y, annotation in enumerate(annotations)
            }
        # # self.approve_coord = None
        # self.reject_coord = None

        state.roi_image.set_value(np.hstack([state.detections_image.value] + rows))
