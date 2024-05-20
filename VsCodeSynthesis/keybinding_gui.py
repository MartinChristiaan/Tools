# %%
# load settings json
from math import e
import os
import json

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

# add vscode keybinding
keybind = ""
while True:
    keybindstr = keybind.replace(" ", "<leader>")
    print(f"current_keybinding : {keybindstr}")
    char = click.getchar()
    if char == "\x03":
        break
    keybind += char
print(keybindstr)
