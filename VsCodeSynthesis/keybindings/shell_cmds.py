# %%
# from symbol import term
from add_vim_keybindings import (
    add_bashrc,
    add_keybindings,
    keybinding,
    terminalCommand,
    vscodeCommand,
)

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
    keybinding(
        "<leader>+f+s",  # file search symbol
        [
            c(
                "cd ~/git/tools/VsCodeSynthesis && bash file_search_symbol.sh ${file}",
                focus=True,
                newTerminal="false",
            )
        ],
    ),
    keybinding(
        "<leader>+d+p",  # run debugtracer
        [
            c(
                "bash ~/git/tools/VsCodeSynthesis/run_debugtracer.sh ${file}",
                focus=True,
                newTerminal="false",
            )
        ],
    ),
    keybinding(
        "<leader>+s+l",  # local search symbol
        [
            c(
                "cd ~/git/tools/VsCodeSynthesis && bash local_search_symbol.sh",
                focus=True,
            )
        ],
    ),
    keybinding(
        "<leader>+q+s",  # quick ssh
        [
            c(
                "cd ~/git/tools/quick_edit && python3 quick_ssh.py",
                focus=True,
            )
        ],
    ),
]

# Run the Python script using the -m syntax and the modified relative path
# Run the Python script using the -m syntax and the modified relative path


def main():

    add_keybindings(keys)
    add_bashrc(keys)


if __name__ == "__main__":
    main()
