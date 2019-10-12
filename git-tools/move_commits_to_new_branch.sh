#/bin/sh

# Moves last N commits to my-new-feature-branch
#
# Example usage:
#     $ ./move_commits_to_new_branch.sh my-new-feature-branch commit-count

if (( $# != 2 )); then
    echo "Illegal number of arguments"
    exit
fi

# Create a new branch (without changing to it), containing all current commits
git branch $1

# Move master back by $commit-count commits
git reset --keep HEAD~$2

# Go to the new branch that still has the desired commits
git checkout $1
