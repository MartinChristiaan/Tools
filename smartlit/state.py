from datetime import datetime
from pathlib import Path
from typing import TypeVar
import numpy as np
from loguru import logger
import pandas as pd

T = TypeVar("T")

from dataclasses import dataclass
from typing import Callable, Generic


def create_logdir(name):
    datestr = datetime.now().strftime("%Y%m%dT%H%M%S")
    logdir = Path(f"./data/logs/{name}/{datestr}/")
    logdir.mkdir(exist_ok=True, parents=True)
    return logdir


class FuncStack:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.stack = []
        self.merger_stack = {}
        self.lock = False
        self.exec_cnt = 0
        self.logdir = create_logdir("funcstack")

    def add_fn(self, fn, merger=False):
        if merger:
            self.merger_stack[fn.__name__] = fn
        else:
            self.stack.append(fn)

    def execute_stack(self):
        logfile = self.logdir / f"{self.exec_cnt}.log"
        if self.lock:
            return
        self.lock = True
        while len(self.stack) + len(self.merger_stack) > 0:
            logger.debug(f"{self.stack}")
            if len(self.stack) > 0:
                fn = self.stack.pop(0)
                fn()
                with open(logfile, "a") as f:
                    f.write(fn.__name__ + "\n")
            else:
                key = list(self.merger_stack.keys())[0]
                fn = self.merger_stack[key]
                fn()
                with open(logfile, "a") as f:
                    f.write(fn.__name__ + "\n")
                del self.merger_stack[key]
        self.lock = False
        self.exec_cnt += 1


from datetime import datetime
from pathlib import Path
import pandas as pd


class ObservableLogger:
    _instance = None  # Class-level variable to store the singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.observables = []
        self.logdir = Path(f"./data/logs/observables/")
        self.logdir.mkdir(exist_ok=True, parents=True)
        datestr = datetime.now().strftime("%Y%m%dT%H%M%S")
        self.logfile = self.logdir / f"{datestr}.csv"

    def observer_update(self):
        data = {"stack_count": stack.exec_cnt}
        for observer in self.observables:
            data = observer.log_state(data)
        print(data)
        df = pd.DataFrame([data])
        df.to_csv(self.logfile, index=False, header=not self.logfile.exists(), mode="a")


stack = FuncStack()
observer_logger = ObservableLogger()


class Observable(Generic[T]):
    def __init__(
        self, value: T, name="observer", log=True, check_if_same=True, **uxprops
    ) -> None:
        self._value = value
        self.subscribers = []
        self.name = name
        self.log = log
        self.runcount = 0
        self.uxprops = uxprops
        self.check_if_same = check_if_same
        if log:
            observer_logger.observables.append(self)

    def set_value(self, new_value):
        if not self.check_if_same or not new_value == self._value:
            self._value = new_value
            self.run()

    def set_value_delayed_run(self, new_value):
        if not self.check_if_same or not new_value == self._value:
            self._value = new_value
            return True
        return False

        # if self.log:
        #     logger.debug(f"set {self.name} with {len(self.subscribers)} subs")
        # [x() for x in self.subscribers]

    def run(self):
        if self.log:
            observer_logger.observer_update()
        for x in self.subscribers:
            stack.add_fn(*x)
        if not stack.lock:
            logger.debug(f"starting stack {self.name}")
            stack.execute_stack()
        self.runcount += 1

    def subscribe(self, fun: Callable, merger=False):
        logger.debug(f"subscribing {fun} to {self.name}")
        self.subscribers.append((fun, merger))

    def log_state(self, data):
        print(f"logging {self.name}")
        data[self.name] = self.value
        return data

    @property
    def value(self) -> T:
        return self._value

    def get_ui_data(self):
        return {"value": self.value, **self.uxprops}


@dataclass
class MouseState:
    event: int
    x: int
    y: int
    flags: int


# class State:
#     def __init__(self):
#         self.timestamps = Observable([], "timestamps")
#         self.frame_index = Observable(0, "frame_index")
#         self.detections = Observable([], name="detections")
#         self.detections_zoomed = Observable([], name="detections_zoomed")
#         self.zoom = Observable(1.0, name="zoom")
#         self.keyboard_event = Observable("", name="keyboard_event")
#         self.mouse_event = Observable(
#             MouseState(0, 0, 0, 0), name="mouse_event", log=False
#         )
#         self.keyboard_mode = Observable("normal", "keyboard_mode")
#         self.current_class = Observable("object", name="current_class")
#         self.frame_inputs = Observable([], name="base_images")
#         self.base_image = Observable([], name="base_image")
#         self.zoomed_image = Observable(np.array([]), name="zoomed_image")
#         self.texted_image = Observable(np.array([]), name="texted_image")
#         self.roi_image = Observable(np.array([]), name="roi_image")
#         self.detections_image = Observable(np.array([]), name="detections_image")
#         self.timestamp = Observable(0.0, name="timestamp")
#         self.image_index = Observable(1, "image_index")

#     def get_runcounts(self):
#         for k, v in self.__dict__.items():
#             print(f"{k}: {v.runcount}")
#         print("________")

# state_instance = State()
