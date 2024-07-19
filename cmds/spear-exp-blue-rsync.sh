#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22' --delete ~/git/projects/spear/  tno@192.168.1.142:/home/tno/git//spear/"; done
	