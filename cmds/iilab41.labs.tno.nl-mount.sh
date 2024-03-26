#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/iilab41.labs.tno.nl/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 22 leeuwenmcv@iilab41.labs.tno.nl:/ /mnt/iilab41.labs.tno.nl/

	