# make sure you have the latest pip
# NOTE: you HAVE to do this upgrade, else pip install won't know what to do without setup.py!
pip3 install --user --upgrade pip
# install xdg-open-wsl using your latest pip
pip install --user git+https://github.com/cpbotha/xdg-open-wsl.git
# ensure that the newly installed xdg-open is active
# the following command should show something like /home/username/.local/bin/xdg-open
which xdg-open
