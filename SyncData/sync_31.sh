
HOST=leeuwenmcv@pc-11393.tsn.tno.nl
PORT=31000

while sleep 1;
 do find ~/git | entr -d bash -c "rsync  -azP -e 'ssh -p $PORT' --delete ~/git/ $HOST:/uhome/leeuwenmcv/git "; 
done
