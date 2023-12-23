# %%
import vscode_commands as v
from add_vim_keybindings import (
    add_keybindings,
    keybinding,
    terminalCommand,
    vscodeCommand,
)

c = vscodeCommand

keys = [
    keybinding("<leader>+r+k", [c("jupyter.restartkernel")]),
    keybinding("<leader>+c+c", [c("jupyter.interactive.clearAllCells")]),
    keybinding("<leader>+i+k", [c("jupyter.interruptkernel")]),
    # keybinding("<leader>+c+a", [c('jupyter.interactive.clearAllCells')]),
]
add_keybindings(keys)
