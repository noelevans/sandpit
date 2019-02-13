'''
Python questions to work on. To invoke with pytest use

    $ python3 answer_template.py
or
    $ python3 -m pytest answer_template.py

'''

import pytest


def inclusive_range(n):
    # For n = 5, return [1, 2, 3, 4, 5]
    return [1, 2, 3, 4, 5]


def average(ol):
    # The mean for a series of numbers
    pass


def no_whitespace(t):
    # Remove all whitespace from the start and end of the string
    pass


def minus_to_plus(t):
    # Replace all - symbols with + characters
    pass


def sum_bar_last(a, b, c):
    # Add a + b and then do it generically for arbitrary arguments
    pass


def mirror(ol):
    # Turn a string around so 1st char is the last, 2nd becomes penultimate
    pass


def odd_idxs(ol):
    # For ol = [4, 5, 6, 7, 8, 9]  return [5, 7, 9] the odd indicies of ol
    pass


def pairs(ol):
    # For a list, return a list of the items in pairs
    # Eg [2, 3, 4, 5, 6, 7, 8, 9] -> [[2, 3], [4, 5], [6, 7], [8, 9]]
    pass


def blank_count(ol):
    # Count the amount of not True elements in ol
    pass


def flatten(ol_of_ol):
    # For [[1, 2, 3], [4, 5, 6], [7, 8]] -> [1, 2, 3, 4, 5, 6, 7, 8]
    pass


def element_divisible_by_3(ol):
    # Is there 1 or more elements divisible by 3 in the input
    pass


def most_common(ol):
    # Return the most common element in the input list
    pass


def dict_reverse(d):
    # For {'a': 3, 'b': 4, 'c': 9} -> {3: 'a', 4: 'b', 9: 'c'}
    pass


###############################################################################
# Validation
###############################################################################


def test_inclusive_range():
    assert list(inclusive_range(5)) == [1, 2, 3, 4, 5]


# def test_average():
#     assert average([2, 2, 2, 3, 4]) == 2.6


# def test_no_whitespace():
#     assert no_whitespace('   hello    ') == 'hello'


# def test_minus_to_plus():
#     assert minus_to_plus('hello-world') == 'hello+world'


# def test_sum_bar_last():
#     assert sum_bar_last(4, 5, 6) == 9


# def test_mirror():
#     assert mirror('smart') == 'trams'


# def test_odd_idxs():
#     assert odd_idxs([1, 2, 3, 4]) == [2, 4]


# def test_pairs():
#     assert pairs([0, 1, 2, 3, 4, 5]) == [[0, 1], [2, 3], [4, 5]]


# def test_blank_count():
#     assert blank_count([7, 0, None, 1, 'hi', '', 88, 0]) == 4


# def test_flatten():
#     assert flatten([[1, 2, 3], [4, 5], [6, 7]]) == [1, 2, 3, 4, 5, 6, 7]


# def test_element_divisible_by_3():
#     assert element_divisible_by_3([1, 2, 4, 5]) == False
#     assert element_divisible_by_3([1, 2, 6, 5]) == True


# def test_most_common():
#     assert most_common([3, 3, 4, 4, 4, 4, 2]) == 4


# def test_dict_reverse():
#     assert dict_reverse({'a': 3, 'b': 4, 'c': 9}) == {3: 'a', 4: 'b', 9: 'c'}


def main():
    import os
    pytest.main([os.path.basename(__file__)])


if __name__ == '__main__':
    main()
