#!/bin/sh

mkdir -p /home/noel/repo/neovim-image/
curl -L https://github.com/neovim/neovim/releases/download/nightly/nvim.appimage > /home/noel/repo/neovim-image/nvim.appimage
chmod +x /home/noel/repo/neovim-image/nvim.appimage
