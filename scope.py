x = 1

def ham(a):
	b = 3
	x = 4
	
	def piglette(c):
		d = b
		global x
		x = 7
		print('In nested function\n===============')
		print locals()
		
	piglette(5)
	print('\nIn function\n===============')
	print locals()
	print x
	print locals()['x']
	print globals()['x']
	
print ('\nGlobals\n===============')
print globals()

ham(2)
