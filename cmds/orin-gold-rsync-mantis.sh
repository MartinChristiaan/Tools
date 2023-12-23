#!/bin/bash
while sleep 0.1; do find ~/git/projects/mantis/  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22'  ~/git/projects/mantis/  dev@iilab29.labs.tno.nl:/home/dev/git/mantis"; done
