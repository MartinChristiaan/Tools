MUSICPATH=/mnt/HardDrive/Media/Music/
FOOBARPATH=/run/user/1000/gvfs/afc:host=00008110-001460D41145801E,port=3/com.foobar2000.mobile
rsync  -rzP --delete $MUSICPATH $FOOBARPATH
