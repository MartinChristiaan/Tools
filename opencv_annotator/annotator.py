from enum import Enum, IntEnum
import cv2
import numpy as np

# from trackertoolbox.detections import Detections
from annotation import Annotation
from drawer import DrawBboxEngine
from mouse_zooming import Zoomer
from roi_drawer import ROIDrawer


class ReturnMode(IntEnum):
    NEXT = 0
    PREV = 1
    STOP = 2


class BoundingBoxAnnotator:
    def __init__(self, image, detections=[]):
        self.image = image
        self.new_annotation = None
        self.is_button_down = False
        self.detections = [x for x in detections if x.real_detection]
        self.drawer = DrawBboxEngine(color_key="class_id", label_keys=["label"])
        self.cur_image = self.image.copy()
        self.drawing_image = self.image.copy()
        self.dirty = True
        self.roi_drawer = ROIDrawer()
        self.zoomer = Zoomer(*self.image.shape[:2])

        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.run_mouse_callbacks)

    def run_mouse_callbacks(self, *args):
        self.draw_rectangle(*args)
        self.zoomer.update_zoom(*args)

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE and self.is_button_down:
            self.cur_image = self.drawing_image.copy()
            self.new_annotation.bbox_w = x - self.new_annotation.bbox_x
            self.new_annotation.bbox_h = y - self.new_annotation.bbox_y
            cv2.rectangle(
                self.cur_image,
                self.new_annotation.upperleft,
                self.new_annotation.downright,
                (0, 255, 0),
                2,
            )

        elif event == cv2.EVENT_LBUTTONDOWN:
            self.new_annotation = Annotation(x, y, 1, 1, 0, "obj", 0)
            self.is_button_down = True

        elif event == cv2.EVENT_LBUTTONUP:
            # self.new_bbox_coords = [self.new_bbox_coords[0], (x, y)]
            self.is_button_down = False
            self.zoomer.compensate_new_annotation(self.new_annotation)
            self.detections.append(self.new_annotation)
            self.dirty = True

    def run(self):
        while True:
            if self.dirty or self.zoomer.dirty:
                image_zoomed = self.zoomer.update_img(self.image)
                if len(self.detections) > 0:
                    detections_zoomed = self.zoomer.update_detections(self.detections)
                    self.cur_image = self.drawer.draw(image_zoomed, detections_zoomed)
                else:
                    self.cur_image = image_zoomed
                self.drawing_image = self.cur_image.copy()
                self.dirty = False
                self.zoomer.dirty = False
                self.cur_image = self.roi_drawer.draw_rois(
                    self.image, self.cur_image, self.detections
                )

            cv2.imshow("image", self.cur_image)
            key = cv2.waitKey(10)
            if key == ord("q"):
                cv2.destroyAllWindows()
                return ReturnMode.STOP
            elif key == ord("d"):
                return ReturnMode.NEXT
            elif key == ord("a"):
                return ReturnMode.PREV


if __name__ == "__main__":
    impath = "./mpv-shot0001.jpg"
    image = cv2.imread(impath)
    bounding_box_selector = BoundingBoxAnnotator(impath)
    bounding_box_selector.run()
