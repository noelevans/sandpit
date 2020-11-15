#!/bin/sh

mkdir -p ~/.vim/swap
mkdir -p ~/.vim/backup
mkdir -p ~/.vim/undo

mkdir ~/repo/
(cd /home/repo/; git clone https://github.com/noelevans/sandpit.git)

git clone --bare https://github.com/noelevans/dotfiles
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.8.0

pip install numpy pandas pylint pyls mypy
pip install git+https://github.com/psf/black.git
pip install pylint mypy pytest

pacman -S tmux git curl
git clone https://aur.archlinux.org/yay-git.git
yay -S neovim-nightly asdf
