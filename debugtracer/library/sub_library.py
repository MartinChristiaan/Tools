from dataclasses import dataclass
import time


def my_sum(a, b):
    return a + b


@dataclass
class ObjectExample:
    a: float
    b: float

    def do_sum(self):
        print("Doing sum...")
        return my_sum(self.a, self.b)
