#!/bin/bash

# Gets the code in your feature-brach updated 
# with the team's head state on the develop branch
#

current_branch=`git rev-parse --abbrev-ref HEAD`

git checkout develop
git merge
git pull origin 
git checkout $current_branch
git merge develop
