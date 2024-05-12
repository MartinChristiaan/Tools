from dataclasses import dataclass
import time
from library.indirect_sum import sum_component


def my_sum(a, b, mode="test"):
    return sum_component(a + b)


@dataclass
class ObjectExample:
    a: float
    b: float

    def do_sum(self, mode="test"):
        print("Doing sum...")
        return my_sum(self.a, self.b)
