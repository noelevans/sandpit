#!/bin/bash

# Gets the code in your feature-brach updated 
# with the team's head state on the develop branch
#
# Example usage:
#     $ ./merge-develop.sh my-feature-branch

if (( $# != 1 )); then
    echo "Illegal number of arguments"
    exit
fi

git checkout develop
git pull origin 
git checkout $1
git merge develop
