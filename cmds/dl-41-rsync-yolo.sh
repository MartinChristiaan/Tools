#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP --delete -e  'ssh -p 10041' ~/git/yolo-plugins/  leeuwenmcv@pc-11393.tsn.tno.nl:/uhome/leeuwenmcv/git/yolo-plugins/ && rsync  -azP --delete -e 'ssh -p 10041' ~/git/dlutils_ii/  leeuwenmcv@pc-11393.tsn.tno.nl:/uhome/leeuwenmcv/git/dlutils_ii/ "; done
