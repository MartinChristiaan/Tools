import json
import os

# convert file to snippet and add them to list!
# File content is body file name is prefix

# Three types
# Remaps
# VS code commands
# Shell commands


def parse_keybinding(keybinding):
    keys = []
    cur_special_key = []
    idx = 0
    in_special_key = False
    while idx < len(keybinding):
        if keybinding[idx] == "<":
            in_special_key = True
            print(in_special_key)
        if in_special_key == True:
            cur_special_key.append(keybinding[idx])
        else:
            keys.append(keybinding[idx])
        if keybinding[idx] == ">":
            in_special_key = False
            keys.append("".join(cur_special_key))
            cur_special_key = []
        idx += 1
    return keys


def update_keybindings():
    home = os.path.expanduser("~")
    setting_base_path = "./settings_base.json"

    with open(setting_base_path, "r") as f:
        text = f.read()
    base_settings = json.loads(text)
    key = "vim.normalModeKeyBindingsNonRecursive"

    # Vs code commands

    vs_commands_folder = "./vsCodeCommands"
    shell_commands_folder = "./ShellCommands"

    for folder in [vs_commands_folder, shell_commands_folder]:
        for filename in os.listdir(folder):
            with open(f"{folder}/{filename}", "r") as f:
                text = f.read()
            shortcuts = text.split("#")
            for shortcut in shortcuts:
                if not len(shortcut.replace(" ", "")) > 0:
                    continue
                name = shortcut.split("\n")[0].replace(" ", "")
                args = shortcut.split("\n")[1].split(":")
                keybinding = args[0]
                command = args[1]

                print(keybinding)
                # print(shortcut.split('\n')[1])
                keys = parse_keybinding(keybinding)
                # print(keys)
                if folder == vs_commands_folder:
                    item = {"before": keys, "commands": [{"command": command}]}
                elif folder == shell_commands_folder:
                    other_args = [False, True, True, False]
                    for i, arg in enumerate(args[2:]):
                        other_args[i] = arg == "True"
                    item = {
                        "before": keys,
                        "commands": [
                            {
                                "command": "terminalCommandKeys.run",
                                "args": {
                                    "cmd": command,
                                    "newTerminal": other_args[0],
                                    "saveAllFiles": other_args[1],
                                    "showTerminal": other_args[2],
                                    "focus": other_args[3],
                                },
                            }
                        ],
                    }
                base_settings[key].append(item)

    tout = json.dumps(base_settings, indent=4)
    home = os.path.expanduser("~")
    vscode_path = f"{home}/.config/Code/User/settings.json"
    if not os.path.exists(vscode_path):
        vscode_path = "/mnt/c/Users/leeuwenmcv/AppData/Roaming/Code/User/settings.json"
        print("Windows path")

    with open(vscode_path, "w") as f:
        f.write(tout)


if __name__ == "__main__":
    update_keybindings()
