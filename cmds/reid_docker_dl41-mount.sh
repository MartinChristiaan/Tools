#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/reid_docker_dl41/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 14119 root@pc-11393.tsn.tno.nl:/ /mnt/reid_docker_dl41/

	