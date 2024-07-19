#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22' --delete ~/git/projects/spear/  leeuwenmcv@iilab42.labs.tno.nl:/home/leeuwenmcv/git//spear/"; done
	