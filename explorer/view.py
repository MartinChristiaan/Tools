import os

from colorama import Back, Fore, Style
from colorama import init as colorama_init
from state import MODES, State

colorama_init()
RESET = Style.RESET_ALL

command_message = """
q  : quit
a  : add bookmark
b  : open bookmark
b  : parent dir
t  : terminal here
e  : explorer here
n  : nautilus here
c  : copy mode (Add path of selected file to clipboard)
p  : paste here (cp path from clipboard here)
fr : rename file
fc : create new file
dc : copy directory
dm : move directory
"""


def get_output_string(state: State):
    s = state
    num_cols = 4
    mode_string = f"{state.mode}"
    if state.path_to_copy != "":
        mode_string += f" ({state.path_to_copy}) "

    output_string = (
        Back.BLUE
        + Fore.WHITE
        + Style.BRIGHT
        + f"{mode_string} | {s.current_folder}".center(25 * num_cols, "-")
        + f"{RESET}\n"
    )

    folder_combos = [x for x in state.combinations if os.path.isdir(x.path.full_path)]
    file_combos = [x for x in state.combinations if not os.path.isdir(x.path.full_path)]
    combinations = folder_combos + file_combos
    keys_entered = len(s.curkey)

    for i, combo in enumerate(combinations):
        keybind_label = f"{combo.keybind[keys_entered:]}".rjust(4)

        item_path = combo.path.full_path
        max_label_length = 20
        item_label = f"{combo.path.shorthand[:max_label_length]}".rjust(20)

        if os.path.isdir(item_path):
            color = Fore.BLUE
        else:
            color = Fore.GREEN
        output_string += (
            f"{Fore.RED}{keybind_label}{RESET} : {color}{item_label}{RESET} | "
        )
        if i % num_cols == num_cols - 1:
            output_string += "\n"
    if len(combinations) == 0:
        output_string += f"{Fore.RED} no items found {RESET} "

    print(output_string)
