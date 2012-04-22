#!/usr/bin/env python

import enchant

d = enchant.Dict('en_US')

def validWord( word ):
	return d.check( word )

def getValidFlips( word, i, alreadyPassed, flips=[] ):
	for ic in range( ord('a'), ord('z') ):
		c = chr( ic )
		if c is not word[i]:
			new_word = word.replace( word[i], c )
			if validWord( new_word ) and new_word not in alreadyPassed:
				flips.append( new_word )
	return flips

def possibleSingleShift( word, alreadyPassed=[] ):
	flips = []
	for i in range(len( word )):
		getValidFlips( word, i, alreadyPassed, flips=flips )
	return flips

def listOfMapsToMap( ol ):
	new_dict = {}
	for li in ol:
		if li:
			new_dict[li.keys()[0]] = li.values()[0]
	return new_dict

def targetFound( tree, target ):
	for leaf in getLeaves( tree ):
		if leaf is target:
			return True
	return False

def noValues( ol ):
	for li in ol:
		if len(li) > 0:
			return False
	return True
	
def getLeaves( tree_list ):
	deepest = {}
	for k in tree_list.keys():
		if tree_list[k]:
			if isinstance( tree_list[k], dict ):
				deepest[tree_list[k].keys()[0]] =  tree_list[k].values()[0]
			else:
				return tree_list[k]
	tree = listOfMapsToMap( deepest.values() )
	if not tree:
		return tree_list.keys()
	return getLeaves( tree )

def flattern( inTree ):
	result = inTree.keys()
	for elem in inTree.values():
		elemValues = flattern( elem )
		result.extend( elemValues )
	return result

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
			print 'possibleSingleShift( leaf ) = ', possibleSingleShift( leaf, flattern( searched ) )
			searched[ leaf ] = possibleSingleShift( leaf, flattern( searched ) )

if __name__ == '__main__':
	print 'Go.'
	snake( 'cat', 'dog' )
	print 'Done!'
