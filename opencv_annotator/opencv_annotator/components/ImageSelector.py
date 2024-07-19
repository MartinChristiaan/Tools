from opencv_annotator.components.text_adder import TextRequest
from opencv_annotator.state import State


class ImageSelector:
    def __init__(self, state: State) -> None:
        self.state = state
        self.index = 0
        state.frame_inputs.subscribe(self.update_image)
        state.keyboard_event.subscribe(self.update_index)
        self.key = ""

    def update_image(self):
        print(" running")
        state = self.state
        self.key = list(state.frame_inputs.value.keys())[self.index]
        state.base_image.set_value(state.frame_inputs.value[self.key])

    def update_index(self):
        state = self.state
        key = state.keyboard_event.value
        image_idx = self.index
        if key == "z":
            image_idx -= 1
            if image_idx < 0:
                image_idx = len(state.frame_inputs.value) - 1
            self.index = image_idx
            self.update_image()

        if key == "x":
            image_idx += 1
            if image_idx == len(state.frame_inputs.value):
                image_idx = 0
            self.index = image_idx
            self.update_image()

    def get_status(self):
        return [
            TextRequest(f"selected_image : {self.key} (z-x)", (255, 255, 255), False)
        ]
