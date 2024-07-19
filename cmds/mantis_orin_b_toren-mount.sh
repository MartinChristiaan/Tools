#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/mantis_orin_b_toren/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 22 leeuwenmcv@192.168.1.141:/ /mnt/mantis_orin_b_toren/

	