import pickle
from click import getchar
from pathlib import Path

previous_state_path = Path("/data/trace_data/previous_state.pkl")
state = None
if previous_state_path.exists():
    with open(previous_state_path, "rb") as f:
        state = pickle.load(f)
from fzf_utils import prompt

if state is None:
    script_options = list(map(Path("/data/trace_data").glob("*")), str)
    script = prompt(script_options, False, "Select script")
    function_options = list(map(script.glob("*")), str)
    function = prompt(function_options, False, "Select function")
    iteration = prompt(range(10), False, "Select iteration")
	state = {"script": script, "function": function, "iteration": iteration}


