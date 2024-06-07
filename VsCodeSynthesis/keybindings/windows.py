# %%
%load_ext autoreload
%autoreload 2
import vscode_commands as v
from add_vim_keybindings import (
    add_keybindings,
    keybinding,
    terminalCommand,
    vscodeCommand,
)

c = vscodeCommand

keys = [
    keybinding("<leader>+c+o", [c('workbench.action.closeOtherEditors')]),
    keybinding("<leader>+c+a", [c('workbench.action.closeAllGroups')]),
    keybinding("<tab>", [c('workbench.action.nextEditor')]),
]
add_keybindings(keys)
