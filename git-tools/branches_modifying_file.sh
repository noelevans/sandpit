#!/bin/sh


# Use this to see branches which have code modifying file $1
# If you remove --source, it yields relevant commits
git log --all --source --$1
