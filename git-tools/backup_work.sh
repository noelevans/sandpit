#!/bin/bash


mkdir -p ../store/`date +%Y%m%d%H%M`
files=$(git status -s | cut -b4-)
echo "$files" | xargs -I{} cp -r --parents "{}" ../store/`date +%Y%m%d%H%M`/