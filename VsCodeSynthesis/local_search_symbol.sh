PWD=$(pwd)
TARGET=$(rg -g '*.py' -i  -p  '(def |class )' $PWD --with-filename --line-buffered --no-heading |fzf --ansi | awk -F ':' '{print $1 ":" $2}')
code -g $TARGET
pen
