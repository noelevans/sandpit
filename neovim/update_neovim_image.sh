#!/bin/sh

mkdir -p ~/repo/neovim-image/
curl -L https://github.com/neovim/neovim/releases/download/nightly/nvim.appimage > ~/repo/neovim-image/nvim.appimage
chmod +x ~/repo/neovim-image/nvim.appimage

# Necessary for coc.nvim plugin
if ! [ -x "$(command -v nodejs)" ]; then
    sudo apt-get install nodejs
fi

# Necessary for coc.nvim plugin
if ! [ -x "$(command -v yarn)" ]; then
    curl --compressed -o- -L https://yarnpkg.com/install.sh | bash
fi

# .bashrc change
if ! [ -x "$(command -v vim | grep nvim)" ]; then
    read -p "Add vim <= neovim alias? " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo 'alias vim=~/repo/neovim-image/nvim.appimage' >> ~/.bashrc
    fi
fi
