#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/orin_b_dev_docker/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 14114 root@iilab34.labs.tno.nl:/ /mnt/orin_b_dev_docker/

	