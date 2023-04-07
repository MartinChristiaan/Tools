#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 11000' --delete ~/git//  leeuwenmcv@pc-11393.tsn.tno.nl:/uhome/leeuwenmcv/git///"; done
	