from opencv_annotator.components.text_adder import TextRequest
from opencv_annotator.state import State
from opencv_annotator.annotation import get_postproc

from typing import List


class PostprocessingHandler:
    def __init__(self, state: State) -> None:
        # self.selected_class = Observable("object")
        self.available_postproc = [
            "none",
            "static",
            "track",
        ]
        # self.image = image
        state.current_class.subscribe(state.zoom.run)
        state.keyboard_event.subscribe(self.keyboard_event)
        self.state = state

    def keyboard_event(self):
        key = self.state.keyboard_event.value
        if key == "p":
            postproc_index = self.state.postproc_index.value
            newvalue = get_next_postproc(postproc_index)
            self.state.postproc_index.set_value(newvalue)

    def get_status(self) -> List[TextRequest]:
        lines = [TextRequest("Postproc selection", (255, 255, 255), True)]
        if self.state.keyboard_mode.value == "normal":
            for i, c in enumerate(self.available_postproc):
                lines.append(
                    TextRequest(
                        f"{i} : {c}",
                        (255, 255, 255),
                        c == self.state.current_class.value,
                    )
                )
        return lines
