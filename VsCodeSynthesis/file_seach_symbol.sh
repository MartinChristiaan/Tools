FILEPATH=$1
TARGET=$(rg -g '*.py' -i  -p  '(def |class )' $FILEPATH --with-filename --line-buffered --no-heading |fzf --ansi | awk -F ':' '{print $1 ":" $2}')
code -g $TARGET
pen
