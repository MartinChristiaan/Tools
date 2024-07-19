TARGET=$(rg -g '*.py' -i  -p  '(def |class )' $HOME/git --with-filename --line-buffered --no-heading |fzf --ansi | awk -F ':' '{print $1 ":" $2}')
code -g $TARGET



#| fzf --ansi #| awk -F ':' '{ system("code " $1) }'
