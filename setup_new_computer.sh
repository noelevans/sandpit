#!/bin/sh

mkdir ~/repo/
(cd /home/repo/; git clone https://github.com/noelevans/sandpit.git)

ln -s ~/repo/sandpit/pylint ~/.pylintrc
ln -s ~/repo/sandpit/start_ipython.py  ~/.ipython/profile_default/startup/start_ipython.py
ln -s ~/repo/sandpit/matplotlibrc .config/matplotlib/matplotlibrc
