import enum
from typing import List
import cv2
from loguru import logger
import numpy as np
from state import Observable, State
from text_adder import TextRequest


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
        ]
        # self.image = image
        state.current_class.subscribe(state.zoom.run)
        state.keyboard_event.subscribe(self.keyboard_event)
        self.state = state

    def keyboard_event(self):
        key = self.state.keyboard_event.value
        if key.isdigit():
            value = int(key)
            if value < len(self.available_classes):
                self.state.current_class.set_value(self.available_classes[value])

    def get_status(self) -> List[TextRequest]:
        lines = [TextRequest("Class selection", (255, 255, 255), True)]
        for i, c in enumerate(self.available_classes):
            lines.append(
                TextRequest(
                    f"{i} : {c}", (255, 255, 255), c == self.state.current_class.value
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
