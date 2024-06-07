from dataclasses import dataclass
import numpy as np
import time
from library.indirect_sum import sum_component
import cv2


def my_sum(a, b, mode="test"):
    return sum_component(a + b)


@dataclass
class ObjectExample:
    a: float
    b: float

    def do_sum(self, mode="test"):
        print(f"Doing sum... {mode}")
        return my_sum(self.a, self.b)

    def do_sum_exception(self):
        # pass
        print("Doing sum exception")
        # raise Exception("test exception")

    def generate_test_image(self):
        return np.ones((128, 128, 3), dtype=np.uint8) * 20

    def process_test_image(self, image):
        return image * 10
