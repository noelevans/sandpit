# map

def add_person(x): return x + " Noel"

greetings = ['Goodmorning', 'Good afternoon', 'Good evening']
map(add_person, greetings)


# filter

def is_noel(x): return x.lower().find('noel') > -1

texts = [
	'is your name not Bruce',
	'pere Noel',
	'my name is noel']
filter(is_noel, texts)

# reduce

def length(x): return len(x)
