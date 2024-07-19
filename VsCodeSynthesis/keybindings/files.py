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

cmd = vscodeCommand("fileutils.duplicateFile")
keys = [
    keybinding("<leader>+d+f", [cmd]),
    keybinding("<leader>+t+f", [vscodeCommand('fileutils.removeFilef')]),
    keybinding("<leader>+c+d", [vscodeCommand('explorer.newFolder')]),
    keybinding("<leader>+f+h", [vscodeCommand('workbench.action.showAllEditorsByMostRecentlyUsed')])



]
add_keybindings(keys)
