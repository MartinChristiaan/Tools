#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 1142' --delete ~/git/projects/spear/  tno@srv.delftdynamics.nl:/home/tno/git//spear/"; done
	