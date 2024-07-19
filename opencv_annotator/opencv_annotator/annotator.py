from enum import IntEnum
import os
import shutil

from click import getchar
import cv2
from matplotlib import pyplot as plt
import pandas as pd
from opencv_annotator.cache_annotator import IOManager
from opencv_annotator.components.PostprocessingHandler import PostprocessingHandler
from opencv_annotator.components.bbox_maker import BBoxMaker
from opencv_annotator.components.class_selection import ClassSelector

# from trackertoolbox.detections import Detections
from opencv_annotator.components.drawer import Drawer
from opencv_annotator.components.ImageSelector import ImageSelector
from opencv_annotator.components.roi_drawer import ROIManager
from opencv_annotator.components.text_adder import ImageTextAdder
from opencv_annotator.components.zoomer import Zoomer
from opencv_annotator.state import MouseState, State


class ReturnMode(IntEnum):
    NEXT = 0
    PREV = 1
    STOP = 2
    SAVE = 3
    IGNORE = 4


import dlutils_ii as du


class BoundingBoxAnnotator:
    def __init__(self, dataset_config: du.DatasetConfig):
        state = State()
        self.io_manager = IOManager(dataset_config, state)
        self.image_selector = ImageSelector(state)
        self.zoomer = Zoomer(state)
        self.bbox_maker = BBoxMaker(state, self.zoomer)
        self.drawer = Drawer(state)
        self.class_selector = ClassSelector(state)
        self.roi_manager = ROIManager(self.zoomer, state)
        self.postproc_handler = PostprocessingHandler(state)
        self.text_adder = ImageTextAdder(
            state,
            [
                self.io_manager.get_status,
                self.class_selector.get_status,
                self.image_selector.get_status,
                self.postproc_handler.get_status,
            ],
        )
        self.state = state

        # cv2.namedWindow("image", flags=cv2.WINDOW_GUI_NORMAL)
        # cv2.namedWindow(
        #     "image",
        #     flags=cv2.WINDOW_FULLSCREEN | cv2.WINDOW_GUI_NORMAL,
        # )
        cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN | cv2.WINDOW_GUI_NORMAL)
        # cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback("image", self.run_mouse_callbacks)

    def run_mouse_callbacks(self, *args):
        state = MouseState(*args[:4])
        self.state.mouse_event.set_value(state)

    def run(self):
        self.drawer.initialized = True
        self.state.frame_index.set_value(self.io_manager.frame_index)
        while True:
            image = self.state.roi_image.value
            cv2.imshow("image", image)
            key = cv2.waitKey(16)
            if key > -1:
                key_str = chr(key)
                print(key_str)
                self.state.keyboard_event.set_value(key_str)

            if key == ord("q"):
                # cv2.destroyAllWindows()
                return

    def save(self):
        config = self.io_manager.dataset_config
        tmp_path = config.pathfinder.annotations_path.with_suffix(".tmp.csv")
        annotations = pd.read_csv(tmp_path)
        config.pathfinder.media_manager.save_annotations(
            annotations, "smallObjectsCorrected", True
        )
        print("saved new annotations")
        shutil.copy(
            self.io_manager.tmp_annotation_path, config.pathfinder.annotations_path
        )
        os.remove(self.io_manager.tmp_annotation_path)

    @staticmethod
    def annotate_config(config):
        # check
        annotator = BoundingBoxAnnotator(config)
        annotator.run()
        del annotator
        # annotator.save()
