import os
import glob
from time import sleep
# Find all data directories remotely
datadirs = glob.glob("/mnt/*/data/leeuwenmcv")
print(datadirs)
home = os.path.expanduser('~')
while True:
	for datadir in datadirs:
		os.system(f"rsync --exclude '*diskstation*' -azP {datadir}/ /data/leeuwenmcv/")
	sleep(5)

	