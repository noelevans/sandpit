import sys

from MapReduce import MapReduce


mr = MapReduce()

def mapper(record):
    bookname, content = record
    for word in content.split():
        mr.emit_intermediate(word, bookname)

def reducer(key, value):
    mr.emit((key, list(set(value))))


def main():
    # Use 'books.json'
    data = open(sys.argv[1])
    mr.execute(data, mapper, reducer)

if __name__ == '__main__':
    main()
