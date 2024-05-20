# %%
# load settings json
from math import e
import os
import json
from typing import List

home = os.path.expanduser("~")
vscode_path = f"{home}/.config/Code/User/settings.json"
if not os.path.exists(vscode_path):
    vscode_path = "/mnt/c/Users/leeuwenmcv/AppData/Roaming/Code/User/settings.json"

with open(vscode_path, "r") as f:
    data = json.load(f)
# %%

key = "vim.normalModeKeyBindingsNonRecursive"

keybindings = data[key]
effects = []
for item in keybindings:
    effect = ""
    if "after" in item:
        effect += ",".join(item["after"])
    if "commands" in item:
        for command in item["commands"]:
            if "command" in command:
                effect += command["command"]
            if "args" in command:
                effect += str(command["args"])
    effects += [effect]
print(effects)
# %%
from fzf_utils import prompt

# selected = prompt(effects)

import click


def get_vscode_command():
    with open(f"{home}/git/tools/VsCodeSynthesis/vscode_commands", "r") as f:
        commands = f.read().split("\n")
    command = prompt(commands)
    return command


def get_keybind() -> List[str]:
    keybind = ""
    while True:
        keybind_list = []
        for x in keybind:
            if x == " ":
                keybind_list += ["<leader>"]
            else:
                keybind_list += [x]
        print(f"current_keybinding : {keybind_list}")
        char = click.getchar()
        # check if char == escape
        if char == "\x1b":
            break
        keybind += char
    return keybind_list


def make_vscode_keybind(keybinds: List[dict]):
    command = get_vscode_command()
    current_keybinds = [x["before"] for x in keybindings]
    while keybind in current_keybinds:
        print("keybinding already exists")
        keybind = get_keybind()

    data = dict(before=keybind, commands=[dict(command=command)])
	keybindings.append(data)
    return keybindings
