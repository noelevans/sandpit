#!/bin/bash


mkdir -p ../store/`date +%Y%m%d%H%M`
files=$(git status | egrep "py|sql|sh|txt" | sed "s/modified://")
echo "$files" | xargs -I{} cp "{}" ../store/`date +%Y%m%d%H%M`/
