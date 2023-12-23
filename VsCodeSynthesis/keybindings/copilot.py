# %%
import vscode_commands as v
from add_vim_keybindings import add_keybindings, keybinding, vscodeCommand

c = vscodeCommand

keys = [
    keybinding("<leader>+c+g", [c("github.copilot.interactiveEditor.generate")]),
]
add_keybindings(keys)
