# Write a shell command which uses fzf and ripgrep to search for a file in all files in the $HOME/git directory and subdirectories which are not ignored by git.
# As output it should give the filename

# Solution:

FILE=$(rg --files $HOME/git | fzf)
code $FILE
