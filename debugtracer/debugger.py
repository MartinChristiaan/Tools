import imp
import os
import pickle
from attr import dataclass
from click import getchar, clear
from pathlib import Path

from sympy import python

from fzf_utils import prompt
import importlib

previous_state_path = Path("/data/trace_data/previous_state.pkl")


def read_pickle(path):
    return pickle.load(open(path, "rb"))


def load_previous_state():
    if previous_state_path.exists():
        with open(previous_state_path, "rb") as f:
            debugger = pickle.load(f)
    else:
        debugger = Debugger()
    return debugger


class ModuleReloader:
    def __init__(self) -> None:
        self.module_timestamps = {}
        self.get_timestamps_modules_last_changed()
        self.imported_modules = {}

    def get_timestamps_modules_last_changed(self):
        python_files = list(Path(os.getcwd()).glob("**/*.py"))
        for python_file in python_files:
            self.module_timestamps[python_file] = python_file.stat().st_mtime

    def reload_is_needed(self):
        should_reload = False
        for module, timestamp in self.module_timestamps.items():
            if timestamp != module.stat().st_mtime:
                should_reload = True
                self.module_timestamps[module] = module.stat().st_mtime
        return should_reload

    def import_or_reload_module(self, module):
        if module in self.imported_modules:
            if self.reload_is_needed():
                imported_module = importlib.reload(self.imported_modules[module])
            else:
                return self.imported_modules[module]
        else:
            imported_module = importlib.import_module(module)
        return imported_module


class Debugger:
    def __init__(self, script=None, function=None, iteration=0) -> None:
        self.script = script
        self.function = function
        self.iteration = iteration
        if self.script is None:
            self.set_script()
        if self.function is None:
            self.set_function()
        self.reloader = ModuleReloader()

    def set_script(self):
        script_options = list(map(str, Path("/data/trace_data").glob("*")))
        self.script = Path(prompt(script_options, False, "Select script"))
        self.set_function()

    def set_function(self):
        function_options = list(map(str, self.script.glob("*")))
        self.function = Path(prompt(function_options, False, "Select function"))
        self.set_iteration()

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
        # run the function
        function_name = meta["name"]
        function = getattr(imported_module, function_name)
        inputs = read_pickle(Path(f"{self.function}/{self.iteration}_input.pkl"))
        args = []
        kwargs = {}
        for k, v in inputs.items():
            if k.startswith("arg"):
                args.append(v)
            else:
                kwargs[k] = v
        result = function(*args, **kwargs)
        print(result)

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
