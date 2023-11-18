# %%
%load_ext autoreload
%autoreload 2
from add_vim_keybindings import (
    add_keybindings,
    vscodeCommand,
    terminalCommand,
    keybinding,
)
import vscode_commands as v

c = vscodeCommand

keys = [
    keybinding("<leader>+c+o", [c('workbench.action.closeOtherEditors')]),
    keybinding("<leader>+c+a", [c('workbench.action.closeAllGroups')]),

]
add_keybindings(keys)
