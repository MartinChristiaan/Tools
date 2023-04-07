#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 61234' --delete ~/git/projects/spear/pipeline/  tno@5.159.32.215:/home/tno/git//spear/pipeline/"; done
	