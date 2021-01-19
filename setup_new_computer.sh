#!/bin/sh

# Run this on new computer with:
# wget -O - https://raw.githubusercontent.com/noelevans/sandpit/master/setup_new_computer.sh | bash

sudo pacman -S git

mkdir -p /home/noel/.vim/swap
mkdir -p /home/noel/.vim/backup
mkdir -p /home/noel/.vim/undo
mkdir /home/noel/repo/

(
    cd /home/noel/repo/;
    git clone https://aur.archlinux.org/yay-git.git;
    git clone https://github.com/noelevans/sandpit.git;
    git clone https://github.com/noelevans/pydantic.git;
    git clone https://github.com/noelevans/pdbpp.git;
    git clone https://github.com/noelevans/black.git;
    git clone https://github.com/noelevans/typing.git;
    git clone https://github.com/noelevans/cpython.git;
    git clone https://github.com/noelevans/neovim.git;
    git clone https://github.com/noelevans/completion-nvim.git;
    git clone https://github.com/noelevans/fancycompleter.git;
    git clone https://github.com/noelevans/noelevans.github.io.git;
    git clone https://github.com/poseidon-coding/poseidon-coding.github.io.git;
)

(
    cd /home/noel/repo/yay-git/;
    makepkg -si
)

# yay won't be available until dotfiles repo has been cloned
source /home/noel/.bash_aliases

git clone --bare https://github.com/noelevans/dotfiles

pip install numpy pandas pylint pyls mypy pylint mypy pytest pdbpp
pip install git+https://github.com/psf/black.git
pip install jedi-language-server

yay -S neovim-git asdf tmux curl pyenv httpie
