from dataclasses import dataclass
import time


def my_sum(a, b, mode="test"):
    return a + b + 4


@dataclass
class ObjectExample:
    a: float
    b: float

    def do_sum(self, mode="test"):
        print("Doing sum...")
        return my_sum(self.a, self.b)
