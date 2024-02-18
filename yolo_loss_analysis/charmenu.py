import os

import numpy as np
from click import getchar


def charmenu(action_lut={}, args={}):
    current_keys = list(action_lut.keys())
    cur_value = ""
    while True:
        for k in current_keys:
            print(f"{k} : {action_lut[k].__name__}")

        cur_value += getchar()
        current_keys = [x for x in current_keys if x.startswith(cur_value)]

        if not len(current_keys):
            current_keys = list(action_lut.keys())
            cur_value = ""
        if len(current_keys) == 1:
            action_lut[current_keys[0]](**args)
            return
        os.system("clear")


if __name__ == "__main__":

    def fun1(x):
        print(f"fun 1 {x}")

    def fun2(x):
        print(f"fun 2 {x}")

    actions = {
        "a": fun1,
        "b": fun2,
    }

    charmenu(action_lut=actions, args={"x": "test arg"})
