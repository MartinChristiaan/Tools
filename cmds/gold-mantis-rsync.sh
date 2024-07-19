#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22' --delete ~/git/projects/mantis/  dev@iilab29.labs.tno.nl:/home/dev/git//mantis/ && rsync  -azP -e 'ssh -p 22' --delete ~/git/projects/temporal_yolov5/  dev@iilab29.labs.tno.nl:/home/dev/git//temporal_yolov5/"; done
