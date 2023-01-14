source host.sh
RDA_LATEST=$(ls -td -- $DATAPATH/$PROJECT/*/*/ | head -n 1)
echo $RDA_LATEST
# cmd.exe /c "start cd C:/git/Tools/videoStepper && python main.py $(ls -td -- $DATA_DIR/*/*/ | head -n 1)"
cmd.exe /c "start cmd /k python C:/git/Tools/videoStepper/main.py $(ls -td -- $DATAPATH/$PROJECT/*/*/ | head -n 1)"