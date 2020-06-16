#!/bin/bash

# To use this with pre-commit rather than the employer's
# pre-commit, do:
#
#     pre-commit install -c .pre-commit-noel.yaml
#
# which will then reference this script

# Remove pdb uses
if grep -q "import .*pdb" $1; then
    echo 'Removing pdb import statements in' $1
    sed -i '/.*import .*pdb/d' $1
fi
if grep -q "pdb.set_trace" $1; then
    echo 'Removing pdb set_trace statements in' $1
    sed -i '/.*pdb.set_trace/d' $1
fi

# Get rid of unused imports
if ! autoflake --check $1; then
    echo 'Organising imports in' $1
    autoflake --in-place $1
fi

# Format module
if ! black --check $1; then
    echo 'Black formatting' $1
    black $1
fi

