#!/bin/sh


# Remove pdb uses
sed -i '/.*import pdb/d' $1
sed -i '/.*pdb.set_trace/d' $1

isort $1
black $1
