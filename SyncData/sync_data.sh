while sleep 10;
	do rsync -azP -e  "ssh -p 31000" --exclude '*diskstation*' leeuwenmcv@pc-11393.tsn.tno.nl:$/data/leeuwenmcv/data//mantis /data/mantis; 
done
