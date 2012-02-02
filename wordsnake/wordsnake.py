#!/usr/bin/env python

import enchant

d = enchant.Dict('en_US')
alreadyPassed = []

def validWord( word ):
	return d.check( word )

def getValidFlips( word, i, flips=[] ):
	for ic in range( ord('a'), ord('z') ):
		c = chr( ic )
		if c is not word[i]:
			new_word = word.replace( word[i], c )
			if validWord( new_word ) and new_word not in alreadyPassed:
				flips.append( new_word )
				alreadyPassed.append( new_word )
	return flips

def possibleSingleShift( word ):
	flips = []
	for i in range(len( word )):
		getValidFlips( word, i, flips=flips )
	return flips

def listOfMapsToMap( ol ):
    new_dict = {}
    for li in ol:
		if li:
			new_dict[li.keys()[0]] = li.values()[0]
    return new_dict

def targetFound( dict, target):
	for leaf in getLeaves( dict ):
		if leaf is target:
			return True
	return False

def noValues( ol ):
	for li in ol:
		if len(li) > 0:
			return False
	return True
	
def getLeaves( dict ):
	deepest = {}
	for k in dict.keys():
		if dict[k]:
			deepest[dict[k].keys()[0]] = dict[k].values()[0]
	map = listOfMapsToMap( deepest.values() )
	if not map:
		return dict.keys()
	return getLeaves( map )

def snake( start, target ):
	count = 0
	searched = { start : {} }
	while not targetFound( searched, target ):
		leaves = getLeaves( searched )
		print 'leaves = ', leaves
		count += 1
		if count == 10:
			return []
		for leaf in leaves:
			print 'possibleSingleShift( leaf ) = ', possibleSingleShift( leaf )
			searched[ leaf ] = possibleSingleShift( leaf )

if __name__ == '__main__':
	print 'Go.'
	snake( 'cat', 'dog' )
	print 'Done!'
