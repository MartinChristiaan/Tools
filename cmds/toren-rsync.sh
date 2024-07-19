#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22' --delete ~/git/projects//  leeuwenmcv@pc-08680.tsn.tno.nl:/uhome/leeuwenmcv/git///"; done
	