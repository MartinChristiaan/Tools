#!/bin/bash
#
# Allow normal users to mount a smb/cifs share
# Place this in sudoers.d/mountcifs:
#
# * ALL=NOPASSWD: /usr/local/bin/smbmount

USAGE()
{
   echo "Usage: $0 [ -u user ] [ -d domain ] [ -r | -w ] host share directory"
   echo "   -u user   # Username for cifs authentication"
   echo "   -d domain # Domainname for cifs authentication"
   echo "   -r        # Make directory readable for everyone"
   echo "   -w        # Make directory writable for everyone (use with care)"
   echo "   host      # Hostname of directory service"
   echo "   share     # Sharename of directory service"
   echo "   directory # Local directory (mountpoint)"
   exit 1
}

if [ `id -u` != 0 ]; then
   exec sudo "$0" "$@"
elif [ "$SUDO_UID" != "" ] && [ "$SUDO_GID" != "" ]; then
   OPTIONS="uid=$SUDO_UID,gid=$SUDO_GID"
   MODES="file_mode=0600,dir_mode=0700"
   while true; do
      if [ "$1" == "-u" ] && [[ "$2" =~ ^[a-zA-Z0-9\.]+$ ]]; then
         SUDO_USER="$2"
         shift 2
      elif [ "$1" == "-d" ] && [[ "$2" =~ ^[a-zA-Z0-9_\.]+$ ]]; then
         OPTIONS="$OPTIONS",domain="$2"
         shift 2
      elif [ "$1" == "-r" ]; then
         MODES="file_mode=0644,dir_mode=0755"
         shift 1
      elif [ "$1" == "-w" ]; then
         MODES="file_mode=0666,dir_mode=0777"
         shift 1
      elif [[ "$1" =~ ^-.*$ ]]; then
         USAGE 1>&2
      else
         break
      fi
   done
   if [ "$#" != 3 ]; then
      USAGE 1>&2
   fi
   OPTIONS="$OPTIONS",user="$SUDO_USER,$MODES"
   exec /sbin/mount.cifs "//$1/$2" "$3" -o "$OPTIONS"
else
   USAGE 1>&2
fi
