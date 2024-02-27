#!/bin/bash
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash -c "rsync  -azP -e 'ssh -p 22' --delete ~/git/projects/schiphol_reid/  leeuwenmcv@starlight4:/home/leeuwenmcv/git//schiphol_reid/"; done
	