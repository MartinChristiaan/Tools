#!/bin/bash
rsync  -azP -e 'ssh -J leeuwenmcv@pc-11393.tsn.tno.nl' --delete ~/git/projects/schiphol_reid/  leeuwenmcv@starlight4:/home/leeuwenmcv/git//schiphol_reid/
