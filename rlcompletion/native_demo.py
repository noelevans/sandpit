import rlcompleter


fruit = 'bananas'
element = 3

# Try: fruit[elem
breakpoint()

completer = rlcompleter.Completer(dict(element=3, fruit='banana'))
print(completer.complete('fruit[ ele', 0))
