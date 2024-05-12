import imp
import pickle
import time
from attr import dataclass
from click import getchar, clear
from pathlib import Path

from sympy import python

from reloader import ModuleReloader
from fzf_utils import prompt

previous_state_path = Path("/data/trace_data/previous_state.pkl")


def read_pickle(path):
    return pickle.load(open(path, "rb"))


def load_previous_state():
    if previous_state_path.exists():
        with open(previous_state_path, "rb") as f:
            debugger = pickle.load(f)
        debugger.reloader = ModuleReloader()
    else:
        debugger = Debugger()
    return debugger


class Debugger:
    def __init__(self, script=None, function=None, iteration=0) -> None:
        self.script = script
        self.function = function
        self.iteration = iteration
        self.reloader = ModuleReloader()
        if self.script is None:
            self.set_script()
        if self.function is None:
            self.set_function()

    def set_script(self):
        script_options = list(map(str, Path("/data/trace_data").glob("*")))
        self.script = Path(prompt(script_options, False, "Select script"))
        self.set_function()

    def set_function(self):
        function_options = list(map(str, self.script.glob("*")))
        self.function = Path(prompt(function_options, False, "Select function"))
        # self.set_iteration()

    def set_iteration(self):
        self.iteration = int(input("Enter iteration: "))
        self.save()

    def save(self):
        with open(previous_state_path, "wb") as f:
            pickle.dump(self, f)

    def run_function(self):
        # import the function and run it
        with open(Path(f"{self.function}/meta.pkl"), "rb") as f:
            meta = pickle.load(f)

        module = meta["module"]
        imported_module = self.reloader.import_or_reload_module(module)
        inputs = read_pickle(Path(f"{self.function}/{self.iteration}_inputs.pkl"))
        function_name = meta["name"]
        is_method = meta["is_method"]
        if not is_method:
            function = getattr(imported_module, function_name)
        else:
            typename = type(inputs["arg0"]).__name__
            object_type = getattr(imported_module, typename)
            function = getattr(object_type, function_name)
        args = []
        kwargs = {}
        for k, v in inputs.items():
            if k.startswith("arg"):
                args.append(v)
            else:
                kwargs[k] = v
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        dt = t1 - t0
        fps = 1 / dt
        print(f"result : {result}, dt : {dt*1000:.2f}ms, fps : {fps:.2f}")

        return result

    def run(self):
        while True:
            # clear()
            ui_str = f"""
current state:
script: {self.script.stem}
function: {self.function.stem}
iteration: {self.iteration}
---------------------------------------------
s : select script
f : select function
i : select iteration	
r : run function
q : quit
			"""
            print(ui_str)
            char = getchar()
            action_lut = {
                "s": self.set_script,
                "f": self.set_function,
                "i": self.set_iteration,
                "r": self.run_function,
                "q": exit,
            }
            action_lut[char]()


if __name__ == "__main__":
    debugger = load_previous_state()
    debugger.run()
