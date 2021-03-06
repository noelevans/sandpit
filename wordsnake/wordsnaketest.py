from wordsnake import flattern, getLeaves, listOfMapsToMap 
from wordsnake import possibleSingleShift, snake, targetFound, validWord

import unittest

class WordSnakeTest( unittest.TestCase ):
		
	def setup( self ):
		pass
	
	def test_validWord( self ):
		self.assertTrue(  validWord( 'hello' ) )
		self.assertFalse( validWord( 'iufhwfb' ) )
	
	def test_listOfMapsToMap( self ):
		self.assertEquals(
			{ 'giraffe' : {}, 'hippo' : {} },
			listOfMapsToMap( 
				[ 
					{ 'giraffe': {} }, 
					{ 'hippo'  : {} }, {} ] ) )
		
	def test_getLeaves( self ):
		self.assertEquals( 
			['giraffe'], 
			getLeaves( { 
				'hi':    { 'bye':  {} }, 
				'hello': { 'ciao': { 'giraffe': {} } },
				'salut': {} } ) )
		self.assertEquals( 
			[ 'hippo', 'giraffe' ] , 
			getLeaves( { 
				'hi':    { 'ciao':        { 'giraffe': {} } },
				'hello': { 'bye':         {} }, 
				'salut': { 'aufwidersen': { 'hippo':   {} } } } ) )
		self.assertEquals(
			[ 'uno', 'due' ],
			getLeaves( {
				'alpha': [ 'uno', 'due' ],
				'beta':  { 'dos' : {} } } ) )
		self.assertEquals(
			[ 'uno', 'due' ],
			getLeaves( {
				'beta':  { 'dos' : {} },
				'alpha': [ 'uno', 'due' ] } ) )
		
	def test_flattern( self ):
		self.maxDiff = None
		self.assertEquals( sorted( [ 'hi', 'ciao', 'giraffe', 'hello', 'bye', 'salut', 'aufwidersen', 'hippo' ] ), 
						   sorted( flattern( { 
								'hi':    { 'ciao':        { 'giraffe': {} } },
								'hello': { 'bye':         {} }, 
								'salut': { 'aufwidersen': { 'hippo':   {} } } 
						   } ) ) )

	def test_possibleSingleShift( self ):
		self.assertEquals( 
			[ 'bat', 'eat', 'fat', 'hat', 'lat', 'mat', 'oat', 'pat', 
			  'rat', 'sat', 'tat', 'vat', 'cit', 'cot', 'cut', 'cwt', 
			  'cab', 'cad', 'cal', 'cam', 'can', 'cap', 'car', 'caw', 'cay'], 
			possibleSingleShift( 'cat' ) )
	
	def test_targetFound( self ):	
		self.assertTrue( targetFound( { 'hi':    { 'bye':  {} }, 
                                        'hello': { 'ciao': { 'giraffe': {} } },
                                        'salut': {} 
                                      }, 'giraffe' ) )
		
	def test_snake( self ):
		self.assertEquals( 
			'dog', 
			snake( 'cat', 'dog' ) )
		
if __name__ == '__main__':
	unittest.main()
