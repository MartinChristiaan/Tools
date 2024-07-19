#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/spear-delft-dynamics-jetson/
sshfs -o allow_other -o identityfile=/home/leeuwenmcv/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect tno@192.168.1.142:/ /mnt/spear-delft-dynamics-jetson/
