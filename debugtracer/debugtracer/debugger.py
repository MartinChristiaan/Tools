import os
import pickle
import time
from click import clear, getchar
from pathlib import Path

from debugtracer.function_data import FunctionData
from debugtracer.reloader import ModuleReloader
from debugtracer.fzf_utils import prompt
from debugtracer.testcode_generator import TestGenerator
from prettytable import PrettyTable

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
    def function_data(self):
        module, is_method, function_name = self.load_metadata()
        inputs = read_pickle(Path(f"{self.function}/{self.iteration}_inputs.pkl"))
        args = []
        kwargs = {}
        for k, v in inputs.items():
            if k.startswith("arg"):
                args.append(v)
            else:
                kwargs[k] = v
        results = read_pickle(Path(f"{self.function}/{self.iteration}_outputs.pkl"))[
            "fn_output"
        ]
        return FunctionData(args, kwargs, results, 1, module, function_name, is_method)

    def run_function(self):
        # import the function and run it
        fndata = self.function_data
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
            # TODO log full traceback
            print(f"error : {e}")
            result = None
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
        return module, is_method, function_name

    def run_pytest(self):
        os.system("pytest")

    def run(self):
        while True:
            # clear()
            state_table = PrettyTable()
            state_table.field_names = ["script", "function", "iteration"]
            state_table.add_row([self.script.stem, self.function.stem, self.iteration])

            state_str = f"""
current state:
{state_table}
            """

            option_menu = PrettyTable()

            keys = ["key : ", "s", "f", "i", "r", "t", "p", "q"]
            actions = [
                "Action :",
                "Select script",
                "Select function",
                "Select iteration",
                "Run function",
                "Generate test",
                "Run pytest",
                "Quit",
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
                "q": exit,
            }
            char = getchar()
            clear()
            if not char in action_lut:
                continue
            action_lut[char]()


if __name__ == "__main__":
    debugger = load_previous_state()
    debugger.run()
