# %%
from add_vim_keybindings import (
    add_keybindings,
    vscodeCommand,
    terminalCommand,
    keybinding,
)
import vscode_commands as v

c = vscodeCommand

keys = [
    keybinding("<leader>+r+k", [c("jupyter.restartkernel")]),
    keybinding("<leader>+c+c", [c("jupyter.interactive.clearAllCells")]),
    # keybinding("<leader>+c+a", [c('jupyter.interactive.clearAllCells')]),
]
add_keybindings(keys)
