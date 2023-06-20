
while sleep 0.1; do find ~/git  -not -path "*/node_modules/*" | entr -d bash rsync_all_jetsons.sh; done
