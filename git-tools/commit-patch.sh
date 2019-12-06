#!/bin/sh

# See changes in commit ${1} relative to previous commit

git diff ${1}~ ${1}
