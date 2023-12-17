from enum import IntEnum
import cv2
from ImageSelector import ImageSelector
from bbox_maker import BBoxMaker
from class_selection import ClassSelector

# from trackertoolbox.detections import Detections
from drawer import Drawer
from roi_drawer import ROIManager
from text_adder import ImageTextAdder
from zoomer import Zoomer
from state import State, MouseState


class ReturnMode(IntEnum):
    NEXT = 0
    PREV = 1
    STOP = 2
    SAVE = 3
    IGNORE = 4


class BoundingBoxAnnotator:
    def __init__(
        self,
    ):
        state = State()
        self.image_selector = ImageSelector(state)
        self.zoomer = Zoomer(state)
        self.bbox_maker = BBoxMaker(state, self.zoomer)
        self.drawer = Drawer(state)
        self.class_selector = ClassSelector(state)
        self.roi_manager = ROIManager(self.zoomer, state)
        self.text_adder = ImageTextAdder(
            state, [self.class_selector.get_status, self.image_selector.get_status]
        )
        self.state = state

        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.run_mouse_callbacks)

    def run_mouse_callbacks(self, *args):
        state = MouseState(*args[:4])
        self.state.mouse_event.set_value(state)

    def run(self, frame_inputs, timestamp, detections):
        self.state.timestamp._value = timestamp
        self.drawer.initialized = False
        self.state.detections.set_value(detections)
        # return
        self.state.frame_inputs.set_value(frame_inputs)
        image_idx = 0
        while True:
            # image = self.roi_drawer.out_image.value
            image = self.state.roi_image.value
            # cv2.destroyAllWindows()
            # if dirty:
            cv2.imshow("image", image)
            key = cv2.waitKey(16)
            if key > -1:
                key_str = chr(key)
                self.state.keyboard_event.set_value(key_str)
            # except:
            # pass

            if key == ord("q"):
                cv2.destroyAllWindows()
                return ReturnMode.STOP
            elif key == ord("d"):
                return ReturnMode.NEXT
            elif key == ord("a"):
                return ReturnMode.PREV


# if self.dirty or self.zoomer.dirty or self.roi_drawer.dirty:
#     imgbase = self.images[self.image_idx]
#     image_zoomed = self.zoomer.update_img(imgbase)
#     if len(self.detections) > 0:
#         detections_zoomed = self.zoomer.update_detections(self.detections)
#         self.cur_image = self.drawer.draw(image_zoomed, detections_zoomed)
#     else:
#         self.cur_image = image_zoomed
#     self.drawing_image = self.cur_image.copy()
#     self.dirty = False
#     self.zoomer.dirty = False
#     self.roi_drawer.dirty = False
#     self.cur_image = self.roi_drawer.draw_rois(
#         self.image, self.cur_image, self.detections
#     )
