from typing import TypeVar

import numpy as np
from opencv_annotator.annotation import Annotation, AnnotationPostproc
from loguru import logger

T = TypeVar("T")

from dataclasses import dataclass
from typing import Callable, Generic


class FuncStack:
    def __init__(self) -> None:
        self.stack = []
        self.merger_stack = {}
        self.lock = False

    def add_fn(self, fn, merger=False):
        if merger:
            self.merger_stack[fn.__name__] = fn
        else:
            self.stack.append(fn)

    def execute_stack(self):
        if self.lock:
            return
        # logger.debug(f"executing stack {self.stack} {self.merger_stack}")
        self.lock = True
        while len(self.stack) + len(self.merger_stack) > 0:
            # logger.debug(f"{self.stack}")
            if len(self.stack) > 0:
                fn = self.stack.pop(0)
                fn()
            else:
                key = list(self.merger_stack.keys())[0]
                fn = self.merger_stack[key]()
                # logger.debug(f"exec {fn} {key}")
                del self.merger_stack[key]
        self.lock = False


stack = FuncStack()


class Observable(Generic[T]):
    def __init__(self, value: T, name="observer", log=True) -> None:
        self._value = value
        self.subscribers = []
        self.name = name
        self.log = log
        self.runcount = 0

    def set_value(self, new_value):
        self._value = new_value
        self.run()
        # if self.log:
        # logger.debug(f"set {self.name} with {len(self.subscribers)} subs")
        # [x() for x in self.subscribers]

    def run(self):
        for x in self.subscribers:
            stack.add_fn(*x)
        if not stack.lock:
            # logger.debug(f"starting stack {self.name}")
            stack.execute_stack()
        self.runcount += 1

    def subscribe(self, fun: Callable, merger=False):
        logger.debug(f"subscribing {fun} to {self.name}")
        self.subscribers.append((fun, merger))

    @property
    def value(self) -> T:
        return self._value


@dataclass
class MouseState:
    event: int
    x: int
    y: int
    flags: int


class State:
    def __init__(self):
        self.timestamps = Observable([], "timestamps")
        self.frame_index = Observable(0, "frame_index")
        self.detections = Observable([], name="detections")
        self.detections_zoomed = Observable([], name="detections_zoomed")
        self.zoom = Observable(1.0, name="zoom")
        self.keyboard_event = Observable("", name="keyboard_event")
        self.mouse_event = Observable(
            MouseState(0, 0, 0, 0), name="mouse_event", log=False
        )
        self.keyboard_mode = Observable("normal", "keyboard_mode")
        self.current_class = Observable("object", name="current_class")
        self.frame_inputs = Observable([], name="base_images")
        self.base_image = Observable([], name="base_image")
        self.zoomed_image = Observable(np.array([]), name="zoomed_image")
        self.texted_image = Observable(np.array([]), name="texted_image")
        self.roi_image = Observable(np.array([]), name="roi_image")
        self.detections_image = Observable(np.array([]), name="detections_image")
        self.timestamp = Observable(0.0, name="timestamp")
        self.image_index = Observable(1, "image_index")
        self.postproc_index = Observable(AnnotationPostproc.NONE, "postproc_index")

    def get_runcounts(self):
        for k, v in self.__dict__.items():
            print(f"{k}: {v.runcount}")
        print("________")


# Usage example
state_instance = State()

# Access default values
# print(state_instance.detections.value)  # Output: []
# print(state_instance.zoom.value)  # Output: 1.0
# print(state_instance.mouse_event.value)  # Output: MouseState()


# class ImageEditor:
#     def __init__(self) -> None:
#         self.out_image: np.ndarray = None
#         self.dirty = True

#     def __call__(self, state: State, image: np.ndarray):
#         self.dirty = False
#         return self.edit(deepcopy(state), image)

#     def edit(self, state: State, image):
#         return state, image

#     def mouse_callback(self, event, x, y, flags, param):
#         pass

#     def backward_pass(self, state: State):
#         return state
