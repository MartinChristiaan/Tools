#!/bin/bash
cd /mnt && find . -maxdepth 1 -type d -empty -delete

mkdir -p /mnt/orin-mantis/
sshfs -o allow_other -o identityfile=/home/martin/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect -p 22 dev@iilab52.labs.tno.nl:/ /mnt/orin-mantis/
	
	