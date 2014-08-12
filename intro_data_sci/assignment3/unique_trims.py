import sys

from MapReduce import MapReduce

mr = MapReduce()


def mapper(record):
    seq_id, nucleotide = record
    mr.emit_intermediate(nucleotide[:-10], None)


def reducer(key, _):
    mr.emit(key)


def main():
    # Use 'dna.json'
    mr.execute(open(sys.argv[1]), mapper, reducer)

if __name__ == '__main__':
    main()
