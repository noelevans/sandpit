#!/bin/sh

mkdir ~/.vim
mkdir ~/.vim/swap
mkdir ~/.vim/backup
mkdir ~/.vim/undo
mkdir -p ~/.config/nvim

mkdir ~/repo/
(cd /home/repo/; git clone https://github.com/noelevans/sandpit.git)

git clone --bare https://github.com/noelevans/dotfiles

ln -s ~/repo/sandpit/pylint ~/.pylintrc
ln -s ~/repo/sandpit/start_ipython.py  ~/.ipython/profile_default/startup/start_ipython.py
ln -s ~/repo/sandpit/matplotlibrc .config/matplotlib/matplotlibrc
ln -s ~/repo/sandpit/.vimrc ~/.vimrc
ln -s ~/repo/sandpit/.gitconfig ~/.gitconfig
ln -s ~/repo/sandpit/.bashrc ~/.bashrc
ln -s ~/repo/sandpit/.cocnvimrc ~/.cocnvimrc
ln -s ~/repo/sandpit/coc-settings.json ~/.config/nvim/coc-settings.json
ln -s ~/repo/sandpit/.pdbrc.py ~/.pdbrc.py
