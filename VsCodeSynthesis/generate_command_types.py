# %%
with open("./vscode_commands", "r") as f:
    text = f.read()
commands = [x for x in text.split("\n") if len(x.strip()) > 0]
print(commands)


# %%
def format_as_constant(name: str):
    characters_to_replace = "./!@#$%%^&*() -:"
    for c in characters_to_replace:
        name = name.replace(c, "_")
    return name.upper()


def format_as_value(name: str):
    return f'"{name}"'


out_str = ""
constants = zip(map(format_as_constant, commands), map(format_as_value, commands))

for c, v in constants:
    out_str += f"{c} = {v}\n"
with open("./vscode_commands.py", "w") as f:
    f.write(out_str)

# %%

import matplotlib.pyplot as plt
import numpy as np
import vscode_commands as v

v.VSCODE_DIFF

# x = Path("sads")


# %%
