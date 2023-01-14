source host.sh
DATA_DIR=$DATAPATH/$PROJECT
cd $(ls -td -- $DATA_DIR/*/*/ | head -n 1) && explorer.exe .