import sys
 
from MapReduce import MapReduce
 
mr = MapReduce()
 
def mapper(record):
    order_id = record[1]
    key = order_id
    mr.emit_intermediate(key, record)
 
def reducer(key, value):
    order = [v for v in value if v[0] == 'order'][0]
    items = [v for v in value if v[0] == 'line_item']
    for i in items:
        mr.emit(order + i)
 
def main():
    # Use 'records.json'
    data = open(sys.argv[1])
    mr.execute(data, mapper, reducer)

if __name__ == '__main__':
    main()
