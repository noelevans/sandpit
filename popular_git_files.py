#!/usr/bin/env python

"""
Usage:
    git log --author='Noel' --stat | ./popular_git_files.py
"""

import collections
import operator
import re
import sys


files = collections.defaultdict(lambda: 0)
for line in sys.stdin.readlines():
    match = re.search('(\S+) +\| +(\d+)', line)
    if match and len(match.groups()) == 2:
        g0, g1 = match.groups()
        g0 = g0[g0.rfind('/') + 1:]
        files[g0] = files[g0] + int(g1)

for el in sorted(files.items(), key=operator.itemgetter(1), reverse=True):
    print(el)
