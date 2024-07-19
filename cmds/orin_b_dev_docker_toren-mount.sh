#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/orin_b_dev_docker_toren/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 14114 root@192.168.1.141:/ /mnt/orin_b_dev_docker_toren/

	