#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/gold_orin/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 22 dev@iilab29.labs.tno.nl:/ /mnt/gold_orin/

	