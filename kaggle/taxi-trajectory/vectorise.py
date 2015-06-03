import math
import numpy as np


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def line_addition(line):
    gps = line.split(",")[-1]

points = [(0,    0), 
          (2.1,  0.1), 
          (2.9,  0.05), 
          (2.85, 2.2), 
          (3.05, 4.1), 
          (2.9,  5.9)]

next_points  = points[1:]
vecs = [np.array(n) - np.array(p) for p, n in zip(points, next_points)]

next_vecs = vecs[1:]
angles = [angle(v, n) for v, n in zip(vecs, next_vecs)]

print vecs, angles    