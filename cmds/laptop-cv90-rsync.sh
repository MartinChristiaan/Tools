#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22' --delete ~/git/projects//  leeuwenmcv@iilab41.labs.tno.nl:/home/leeuwenmcv/git///"; done
	