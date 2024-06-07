import os
import pickle
import time
from click import clear, getchar
from pathlib import Path

from sympy import re

from debugtracer.function_data import FunctionData
from debugtracer.reloader import ModuleReloader
from debugtracer.fzf_utils import prompt
from debugtracer.testcode_generator import TestGenerator
from prettytable import PrettyTable
import traceback

previous_state_path = Path("/data/trace_data/previous_state.pkl")


def read_pickle(path):
    return pickle.load(open(path, "rb"))


def load_previous_state():
    if previous_state_path.exists():
        with open(previous_state_path, "rb") as f:
            debugger = pickle.load(f)
        debugger.reloader = ModuleReloader()
        debugger.test_generator = TestGenerator()
    else:
        debugger = Debugger()
    return debugger


class Debugger:
    def __init__(self, script=None, function=None, iteration=0) -> None:
        self.script = script
        self.function = function
        self.iteration = iteration
        self.reloader = ModuleReloader()
        self.test_generator = TestGenerator()
        if self.script is None:
            self.set_script()
        if self.function is None:
            self.set_function()
        self._fndata_cache = {}
        self.max_iteration = 0
        self.stopped = False

    def set_script(self):
        script_options = list(map(str, Path("/data/trace_data").glob("*")))
        self.script = Path(prompt(script_options, False, "Select script"))
        self.set_function()

    def set_function(self):
        function_options = list(map(str, self.script.glob("*")))
        self.function = Path(prompt(function_options, False, "Select function"))
        self.iteration = 0
        # self.set_iteration()

    def set_iteration(self):
        self.iteration = int(input("Enter iteration: "))
        while self.iteration > self.max_iteration:
            print(f"iteration {self.iteration} does not exist")
            self.iteration = int(input("Enter iteration: "))
        self.save()

    def save(self):
        with open(previous_state_path, "wb") as f:
            pickle.dump(self, f)

    def generate_test(self, testname=None, description=None):

        fndata = self.function_data
        if testname is None:
            testname = input("name : ")
        if description is None:
            description = input("description : [default = auto]")
            if (
                len(description) == 0
                or description == "auto"
                or description == "default"
                or description == "d"
            ):
                description = "auto"
        self.test_generator.generate_test_from_function_data(
            testname, description, fndata
        )

    @property
    def function_data(self) -> FunctionData:
        key = str(self.function) + str(self.iteration)
        if not key in self._fndata_cache:
            module, is_method, function_name = self.load_metadata()
            inputs = read_pickle(Path(f"{self.function}/{self.iteration}_inputs.pkl"))
            args = []
            kwargs = {}
            for k, v in inputs.items():
                if k.startswith("arg"):
                    args.append(v)
                else:
                    kwargs[k] = v

            results_path = Path(f"{self.function}/{self.iteration}_outputs.pkl")
            results = (
                read_pickle(results_path)["fn_output"]
                if results_path.exists()
                else None
            )
            self._fndata_cache[key] = FunctionData(
                args, kwargs, results, 1, module, function_name, is_method
            )
        return self._fndata_cache[key]

    def run_function(self):
        # import the function and run it
        fndata = self.function_data
        for module in self.reloader.get_imported_modules():
            self.reloader.import_or_reload_module(module.__name__)
        imported_module = self.reloader.import_or_reload_module(fndata.module)

        if not fndata.is_method:
            function = getattr(imported_module, fndata.name)
        else:
            typename = type(fndata.args[0]).__name__
            object_type = getattr(imported_module, typename)
            function = getattr(object_type, fndata.name)
        t0 = time.time()
        try:
            result = function(*fndata.args, **fndata.kwargs)
        except Exception as e:
            traceback.print_exc()
            print(f"error : {e}")
            result = "error"
        t1 = time.time()
        dt = t1 - t0
        fps = 1 / dt
        print(f"result : {result}, dt : {dt*1000:.2f}ms, fps : {fps:.2f}")
        return result

    def load_metadata(self):
        with open(Path(f"{self.function}/meta.pkl"), "rb") as f:
            meta = pickle.load(f)
        module = meta["module"]
        is_method = meta["is_method"]
        function_name = meta["name"]
        self.max_iteration = meta["iteration"]
        return module, is_method, function_name

    def run_pytest(self):
        os.system("pytest")

    def decrement_iteration(self):
        self.iteration -= 1
        if self.iteration < 0:
            self.iteration = self.max_iteration
        self.save()

    def increment_iteration(self):
        self.iteration += 1
        if self.iteration > self.max_iteration:
            self.iteration = 0
        self.save()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            inputs = {f"arg{i}": arg for i, arg in enumerate(self.function_data.args)}
            inputs.update(self.function_data.kwargs)
            # clear()
            state_table = PrettyTable()
            state_table.field_names = ["script", "function", "iteration"] + list(
                inputs.keys()
            )
            state_table.add_row(
                [self.script.stem, self.function.stem, self.iteration]
                + list(str(x)[:100] for x in inputs.values())
            )

            state_str = f"""
current state:
{state_table}
            """

            option_menu = PrettyTable()

            keys = ["key : ", "s", "f", "i", "r", "t", "p", "q", "j", "k"]
            actions = [
                "Action :",
                "Select script",
                "Select function",
                "Select iteration",
                "Run function",
                "Generate test",
                "Run pytest",
                "Quit",
                "decrement iteration",
                "increment iteration",
            ]
            option_menu.field_names = keys
            option_menu.add_row(actions)
            print(state_str + "\n" + str(option_menu))

            action_lut = {
                "s": self.set_script,
                "f": self.set_function,
                "i": self.set_iteration,
                "r": self.run_function,
                "t": self.generate_test,
                "p": self.run_pytest,
                "q": self.stop,
                "j": self.decrement_iteration,
                "k": self.increment_iteration,
            }
            char = getchar()
            clear()
            if not char in action_lut:
                continue
            action_lut[char]()


if __name__ == "__main__":
    debugger = load_previous_state()
    debugger.run()
