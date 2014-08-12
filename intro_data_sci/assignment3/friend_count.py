import sys

from MapReduce import MapReduce


mr = MapReduce()

def mapper(record):
    person, follower = record
    mr.emit_intermediate(person, follower)

def reducer(key, value):
    mr.emit((key, len(value)))

def main():
    # Use 'friends.json'
    mr.execute(open(sys.argv[1]), mapper, reducer)

if __name__ == '__main__':
    main()
