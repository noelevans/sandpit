#!/bin/bash


# Remove pdb uses
if grep -q "import .*pdb" $1; then
    sed -i '/.*import .*pdb/d' $1
fi
if grep -q "pdb.set_trace" $1; then
    sed -i '/.*pdb.set_trace/d' $1
fi

# Get rid of unused imports
if ! autoflake --check $1; then
    autoflake --in-place $1
fi

# Format module
if ! black --check $1; then
    black $1
fi

