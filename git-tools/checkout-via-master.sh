#!/bin/sh

git checkout master
git pull
git checkout -b $1
