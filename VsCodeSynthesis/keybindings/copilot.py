# %%
from add_vim_keybindings import (
    add_keybindings,
    vscodeCommand,
    keybinding,
)
import vscode_commands as v

c = vscodeCommand

keys = [
    keybinding("<leader>+c+g", [c("github.copilot.interactiveEditor.generate")]),
]
add_keybindings(keys)
