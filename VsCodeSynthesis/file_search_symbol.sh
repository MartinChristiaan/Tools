FILEPATH=$1
TARGET=$(rg -g '*.py' -i  -p  '(def |class )' $FILEPATH --line-buffered --no-heading |fzf --ansi)
lineno=$(echo $TARGET | cut -d ':' -f 1)
code -g $FILEPATH:$lineno

