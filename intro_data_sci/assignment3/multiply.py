import sys

from MapReduce import MapReduce


width  = 5
height = 5
mr = MapReduce()

def mapper(record):
    name, row, col, value = record
    if name == 'a':
        for n in range(width):
            mr.emit_intermediate((row, n), record)
    else:
        for n in range(height):
            mr.emit_intermediate((n, col), record)

def reducer(key, values):
    a = [v for v in values if v[0] == 'a']
    b = [v for v in values if v[0] == 'b']
    total = 0
    for m in a:
        for n in b:
            if n[1] == m[2]:
                total = total + n[-1] * m[-1]
    mr.emit((key[0], key[1], total))

def main():
    # Use 'matrix.json'
    mr.execute(open(sys.argv[1]), mapper, reducer)

if __name__ == '__main__':
    main()
