import sys

from MapReduce import MapReduce


mr = MapReduce()

def mapper(record):
    person, follower = record
    first = min(person, follower)
    last  = max(follower, person)
    mr.emit_intermediate(first, last)

def reducer(key, values):
    asymmetrics = [el for el in values if values.count(el) == 1]
    for a in asymmetrics:
        mr.emit((key, a))
        mr.emit((a, key))

def main():
    # Use 'friends.json'
    mr.execute(open(sys.argv[1]), mapper, reducer)

if __name__ == '__main__':
    main()
