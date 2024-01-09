from typing import List

import cv2
import numpy as np
from opencv_annotator.components.text_adder import TextRequest
from loguru import logger
from opencv_annotator.state import Observable, State


class ClassSelector:
    def __init__(self, state: State) -> None:
        # self.selected_class = Observable("object")
        self.available_classes = [
            "object",
            "person",
            "vehicle",
            "drone",
            "ignore_area",
            "ignore_frame",
            "boat",
            "bycicle",
            "animal",
            "ignore_area_seq",
        ]
        # self.image = image
        state.current_class.subscribe(state.zoom.run)
        state.keyboard_event.subscribe(self.keyboard_event)
        self.state = state

    def keyboard_event(self):
        key = self.state.keyboard_event.value
        if key.isdigit() and self.state.keyboard_mode.value == "normal":
            value = int(key)
            if value < len(self.available_classes):
                self.state.current_class.set_value(self.available_classes[value])

    def get_status(self) -> List[TextRequest]:
        lines = [TextRequest("Class selection", (255, 255, 255), True)]
        if self.state.keyboard_mode.value == "normal":
            for i, c in enumerate(self.available_classes):
                lines.append(
                    TextRequest(
                        f"{i} : {c}",
                        (255, 255, 255),
                        c == self.state.current_class.value,
                    )
                )
        return lines

    # def add_class_label(self):
    #     state = self.state
    #     out = cv2.putText(
    #         state.zoomed_image.value,
    #         state.current_class.value,
    #         (10, 30),
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #         1,
    #         (255, 255, 255),
    #         2,
    #     )
    #     state.texted_image.set_value(out)
