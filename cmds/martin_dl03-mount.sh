#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/martin_dl03/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 10314 root@pc-11393:/ /mnt/martin_dl03/

	