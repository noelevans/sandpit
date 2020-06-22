#!/bin/sh

git stash --keep-index
git commit
git add -u
git commit
