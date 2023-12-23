#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/xavier1-ib-ibotics/
sshfs -o allow_other -o identityfile=/home/martin/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 22 ibotics@iilab24.labs.tno.nl:/ /mnt/xavier1-ib-ibotics/
