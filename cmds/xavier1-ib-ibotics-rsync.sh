#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22' --delete ~/git/v2119/  ibotics@iilab24.labs.tno.nl:/home/ibotics/git//v2119/"; done
