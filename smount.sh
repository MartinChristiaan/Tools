#!/bin/bash
smount () {
	sshfs -o allow_other -o identityfile=/home/martin/.ssh/id_rsa -o ServerAliveInterval=1 -o reconnect $REMOTE $LOCAL
}