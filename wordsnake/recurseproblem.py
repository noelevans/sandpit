#!/usr/bin/env python

def flattern( inTree ):
    result = inTree.keys()
    for elem in inTree.values():
        elemValues = flattern( elem )
        result.extend( elemValues )
    return result

print flattern( {'ciao':{'giraffe':{}}} )

print flattern( { 'hi':    { 'ciao':        { 'giraffe': {} } },
                  'hello': { 'bye':         {} }, 
                  'salut': { 'aufwidersen': { 'hippo':   {} } } 
                } )
