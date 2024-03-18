from opencv_annotator.components.text_adder import TextRequest
from opencv_annotator.state import State
from opencv_annotator.annotation import index_to_postproc, postproc_to_index

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
            postproc = self.state.postproc_index.value
            newvalue = index_to_postproc(postproc_to_index(postproc) + 1)
            print("updating")
            self.state.postproc_index.set_value(newvalue)

    def get_status(self) -> List[TextRequest]:
        lines = [TextRequest("Postproc selection (p)", (255, 255, 255), True)]
        if self.state.keyboard_mode.value == "normal":
            for i, c in enumerate(self.available_postproc):
                lines.append(
                    TextRequest(
                        f"{i} : {c}",
                        (255, 255, 255),
                        i == postproc_to_index(self.state.postproc_index.value),
                    )
                )
        return lines
