# %%
from add_vim_keybindings import (
    add_bashrc,
    add_keybindings,
    vscodeCommand,
    terminalCommand,
    keybinding,
)

# from symbol import term
import vscode_commands as v

c = terminalCommand

keys = [
    keybinding(
        "<leader>+c+s",
        [c("cd ~/git/tools/VsCodeSynthesis && bash create_snippet.sh", focus=True)],
    ),
    keybinding(
        "<leader>+r+i",
        [
            c(
                "autoflake --in-place --remove-all-unused-imports ${file} ",
                focus=False,
            )
        ],
    ),
    keybinding(
        "<leader>+t+m",
        [
            c(
                "tmux",
                focus=False,
            )
        ],
    ),
    keybinding(
        "<leader>+a+t",  # add tool
        [
            c(
                "cd ~/git/tools/VsCodeSynthesis && python3 add_tool.py",
                focus=True,
            )
        ],
    ),
    keybinding(
        "<leader>+e+t",  # add tool
        [
            c(
                "cd ~/git/tools/VsCodeSynthesis && python3 edit_tool.py",
                focus=True,
            )
        ],
    ),
    keybinding(
        "<leader>+g+s+f",  # git search file
        [
            c(
                "cd ~/git/tools/VsCodeSynthesis && bash filesearch.sh",
                focus=True,
            )
        ],
    ),
    keybinding(
        "<leader>+g+s+s",  # git search symbol
        [
            c(
                "cd ~/git/tools/VsCodeSynthesis && bash git_search_symbol.sh",
                focus=True,
            )
        ],
    ),
]
add_keybindings(keys)
add_bashrc(keys)
