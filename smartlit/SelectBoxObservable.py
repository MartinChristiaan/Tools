from state import Observable


from typing import Any


class SelectBoxObservable(Observable):
    def __init__(
        self, value: Any, name="observer", log=True, options=[], **uxprops
    ) -> None:
        self.options = options
        super().__init__(value, name, log, uimode="selectbox")

    def get_ui_data(self):
        data = super().get_ui_data()
        data["options"] = self.options
        return data
