import os
import glob
from time import sleep
# Find all data directories remotely

# gitdirs = glob.glob("/mnt/*/home/leeuwenmcv")
host= "leeuwenmcv@pc-11393.tsn.tno.nl"
home = os.path.expanduser('~')
os.system(f"while sleep 1; do find ~/git | entr -d bash -c \"rsync  -azP -e 'ssh -p 31000' --delete ~/git/  {host}:/uhome/leeuwenmcv/git \"; done")


	