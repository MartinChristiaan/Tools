FILEPATH=$1
TARGET=$(rg -g '*.py' -i  -p  '(def |class )' $FILEPATH  --line-buffered --no-heading |fzf --ansi | awk -F ':' '{print $FILE ":" $2}')
code -g $TARGET
