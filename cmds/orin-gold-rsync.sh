#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22' --delete ~/git/projects/v2119/  dev@iilab29.labs.tno.nl:/home/dev/git//v2119/"; done
	