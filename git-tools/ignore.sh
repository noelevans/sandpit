#!/bin/sh

# Ignore a file (that is tracked) from being committed from repo

git update-index --assume-unchanged ${1}
