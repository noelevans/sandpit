#!/bin/bash


git status | grep "\.py" | \
sed "s/new file://" | sed "s/modified://" | \
xargs -L 1 echo black
