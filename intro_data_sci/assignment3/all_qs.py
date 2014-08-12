from MapReduce import MapReduce

class InvertedLookupMapReduce(MapReduce):
    
    def mapper(self, record):
        book_name, content = record
        for word in content.split():
            self.emit_intermediate(word, book_name)
    
    def reducer(self, key, value):
        self.emit((key, value))

    
class RelationalJoinMapReduce(MapReduce):
    
    def mapper(self, record):
        _type    = record[0]
        order_id = record[1]
        pk_id    = record[2]
        if _type == 'order':
            key = (_type, order_id)
        else:
            key = (_type, order_id, pk_id)
        self.emit_intermediate(key, record)
        
    def reducer(self, key, value):
        if key[0] == 'line_item':
            corresponding_lines = self.intermediate[('order', key[1])]
            for line in corresponding_lines:
                tmp = line
                tmp.extend(value[0])
                self.emit(tmp)


class CountFriendsMapReduce(MapReduce):
    
    def mapper(self, record):
        person, follower = record
        self.emit_intermediate(person, follower)
        
    def reducer(self, key, value):
        self.emit((key, len(value)))
        
        
class AsymmetricFriendsMapReduce(MapReduce):
    
    #def __init__(self):
        #self.intermediate = {}
        #self.result = set()
    
    def mapper(self, record):
        person, follower = record
        self.emit_intermediate((person, follower), None)
        self.emit_intermediate((follower, person), None)
    
    # def emit(self, value):
        # self.result.add(value)
        
    def reducer(self, key, values):
        self.emit((key[0], key[1]))

    
def main():
    mr1 = InvertedLookupMapReduce()
    data    = open('books.json')
    mapper  = mr1.mapper
    reducer = mr1.reducer
    # mr1.execute(data, mapper, reducer)
        
    mr2 = RelationalJoinMapReduce()
    data    = open('records.json')
    mapper  = mr2.mapper
    reducer = mr2.reducer
    # mr2.execute(data, mapper, reducer)
    
    mr3  = CountFriendsMapReduce()
    data = open('friends.json')
    # mr3.execute(data, mr3.mapper, mr3.reducer)
    
    mr4  = AsymmetricFriendsMapReduce()
    data = open('friends.json')
    mr4.execute(data, mr4.mapper, mr4.reducer)

if __name__ == '__main__':
    main()
