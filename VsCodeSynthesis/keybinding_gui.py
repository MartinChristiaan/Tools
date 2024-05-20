# %%
# load settings json
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
for k in keybindings:
    print(k)
