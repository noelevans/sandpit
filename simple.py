import re
import string

def asl(age, sex, location):
	print "%d/%s/%s" % (age, sex, location)


asl(29, 'M', 'London')

# passing args as a tuple
tup = (29, 'M', 'London')
asl(*tup)

# passing args as a dictionary
dict = {'location':'Hereford', 'sex':'M', 'age':18}
asl(**dict)


# reading file
try:
	f = open('simple.csv', 'r')
	# for username, clazz, name, year,vegetarian in f.readlines().split(','):
	for line in f.readlines():
		line.rstrip('\n')
finally:
	f.close


alpha_to_num = string.maketrans('abcdef', '123456')
"He's a very naughty boy".translate(alpha_to_num)

def containsAll(testStr, these):
	identity = string.maketrans('', '')
	return not testStr.translate(identity, these)

containsAll('abcdefghij', 'defghijabc')


words = ['Hello', 'World', 'and', 'Noel']
' '.join(words)

