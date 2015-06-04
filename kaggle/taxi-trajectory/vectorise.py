import math
import numpy as np
import re


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))


def length(v):
  return math.sqrt(dotproduct(v, v))


def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def vectors(line):
    floats = lambda m: [float(n) for n in m.split(',')]
    gps = [floats(m) for m in re.findall('[\d\.-]+,[\d\.-]+', line)]

    next_gps  = gps[1:]
    return [np.array(n) - np.array(p) for p, n in zip(gps, next_gps)]


def lengths(vecs):
    return [length(v) for v in vecs]


def angles(vecs):
    next_vecs = vecs[1:]
    return [angle(v, n) for v, n in zip(vecs, next_vecs)]


filename     = 'train.small.csv'
new_filename = 'train.extra.small.csv'

with open(new_filename, 'w') as f:
    for n, line in enumerate(open(filename)):
        if n == 0:
            print 'a'
            print line 
            print 'a'
            new_line = line
        else:
            vecs = vectors(line)
            lengths_ = '"' + str(lengths(vecs)) + '"'
            angles_ = '"' + str(angles(vecs)) + '"'
            new_line = line + ',' +  lengths_ + ',' + angles_ + '\n'
        f.write(new_line)