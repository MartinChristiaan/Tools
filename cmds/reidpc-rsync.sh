#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22' --delete ~/git/projects/schiphol_reid/  reid@iilab28.labs.tno.nl:/home/reid/git//schiphol_reid/"; done
	