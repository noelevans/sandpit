#!/bin/sh

# Show the patch of how the current state of the repo differs
# from the SHA on master when the branch was created

# Alternative method:
#     git diff `git merge-base --fork-point master`

git diff master...

