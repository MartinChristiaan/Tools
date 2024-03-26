#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/mantis_orin_b_docker/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 8008 root@iilab34.labs.tno.nl:/ /mnt/mantis_orin_b_docker/

	