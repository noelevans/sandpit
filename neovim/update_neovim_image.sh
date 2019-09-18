#!/bin/sh

mkdir -p ~/repo/neovim-image/
curl -L https://github.com/neovim/neovim/releases/download/nightly/nvim.appimage > ~/repo/neovim-image/nvim.appimage
chmod +x ~/repo/neovim-image/nvim.appimage
