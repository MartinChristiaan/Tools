rm /tmp/dest/ > null 2>&1
python3 ~/git/tools/explorer/os_explorer.py
cd $(cat /tmp/dest)
# check if tmp exists, if so go there
