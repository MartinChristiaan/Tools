import pickle
from attr import dataclass
from click import getchar, clear
from pathlib import Path

from fzf_utils import prompt

previous_state_path = Path("/data/trace_data/previous_state.pkl")


def load_previous_state():
    if previous_state_path.exists():
        with open(previous_state_path, "rb") as f:
            debugger = pickle.load(f)
    else:
        debugger = Debugger()
    return debugger


class Debugger:
    def __init__(self, script=None, function=None, iteration=0) -> None:
        self.script = script
        self.function = function
        self.iteration = iteration
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
        self.set_iteration()

    def set_iteration(self):
        self.iteration = int(input("Enter iteration: "))
        self.save()

    def save(self):
        with open(previous_state_path, "wb") as f:
            pickle.dump(self, f)
	
    def run_function(self):
		# import the function and run it


    def run(self):
        while True:
            clear()
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
