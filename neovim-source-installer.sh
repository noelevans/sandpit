#!/bin/sh


PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

git clone https://github.com/neovim/neovim.git ~/repo/neovim-new-build
cd ~/repo/neovim-new-build/
make CMAKE_EXTRA_FLAGS="-DCMAKE_INSTALL_PREFIX=$HOME/neovim"

if [ ! -f ~/repo/neovim-new-build/build/bin/nvim ]; then
    echo "Failed: incomplete build!"
    exit 2
fi

# mv ~/repo/neovim-new-build ~/repo/neovim

