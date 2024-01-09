# %%
from dataclasses import dataclass
from typing import Callable, List

import cv2
from opencv_annotator.state import State


@dataclass
class TextRequest:
    text: str
    color: tuple
    bold: bool


class ImageTextAdder:
    def __init__(
        self,
        state: State,
        sources: List[Callable] = [],
        font=cv2.FONT_HERSHEY_SIMPLEX,
        font_size=0.5,
        font_thickness=1,
    ):
        self.font = font
        self.font_size = font_size
        self.font_thickness = font_thickness
        self.state = state
        self.sources = sources
        state.zoomed_image.subscribe(self.add_texts)
        state.keyboard_mode.subscribe(self.add_texts)

    def add_text_to_image(
        self, image, text_requests: List[TextRequest], position=(10, 30)
    ):
        for request in text_requests:
            font_thickness = (
                self.font_thickness if not request.bold else self.font_thickness * 2
            )

            cv2.putText(
                image,
                request.text,
                position,
                self.font,
                self.font_size,
                request.color,
                font_thickness,
            )

            # Increment the Y coordinate for the next line
            position = (position[0], position[1] + int(30 * self.font_size))

        return image

    def add_texts(self):
        state = self.state
        text_requests = []
        for source in self.sources:
            text_requests += source()
        image = state.zoomed_image.value
        self.add_text_to_image(image, text_requests)
        state.texted_image.set_value(image)
