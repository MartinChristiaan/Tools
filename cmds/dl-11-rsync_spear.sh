#!/bin/bash
while sleep 0.1; do find ~/git/projects/spear/  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 11000' --delete ~/git/projects/spear/  leeuwenmcv@pc-11393.tsn.tno.nl:/uhome/leeuwenmcv/git/spear/"; done
