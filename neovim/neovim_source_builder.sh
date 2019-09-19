#! /bin/bash

SRCDIR=~/repo/neovim

function init_nvim()
{
    echo `pwd`
    rm -rf * .deps;
    git reset --hard
    git pull --rebase
}

function build_nvim()
{
    if [  "${HOME: -1}" == "/" ]; then
        export HOME=${HOME:0:-1}
    fi
    make CMAKE_BUILD_TYPE=RelWithDebInfo CMAKE_EXTRA_FLAGS="-DCMAKE_INSTALL_PREFIX=${HOME}/local"
}

function install_nvim()
{
    cd $SRCDIR || exit 1
    killall nvim
    make install
}

cd $SRCDIR || exit 1

which gcc-9 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    export CXX=gcc++-9
fi

init_nvim
build_nvim || exit 1
install_nvim
