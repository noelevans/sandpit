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


def test_inclusive_range():
    assert list(inclusive_range(5)) == [1, 2, 3, 4, 5]


def average(ol):
    # The mean for a series of numbers
    pass


# def test_average():
#     assert average([2, 2, 2, 3, 4]) == 2.6


def no_whitespace(t):
    # Remove all whitespace from the start and end of the string
    pass


# def test_no_whitespace():
#     assert no_whitespace('   hello    ') == 'hello'


def minus_to_plus(t):
    # Replace all - symbols with + characters
    pass


# def test_minus_to_plus():
#     assert minus_to_plus('hello-world') == 'hello+world'


def sum_bar_last(a, b, c):
    # a + b - c and then do it generically for arbitrary arguments
    pass


# def test_sum_bar_last():
#     assert sum_bar_last(4, 5, 6) == 3
#     assert sum_bar_last(4, 5, 1, 6) == 4


def mirror(s):
    # Turn a string around so 1st char is the last, 2nd becomes penultimate
    pass


# def test_mirror():
#     assert mirror('smart') == 'trams'


def odd_idxs(ol):
    # For ol = [4, 5, 6, 7, 8, 9]  return [5, 7, 9] the odd indicies of ol
    pass


# def test_odd_idxs():
#     assert odd_idxs([1, 2, 3, 4]) == [2, 4]


def pairs(ol):
    # For a list, return a list of the items in pairs
    # Eg [2, 3, 4, 5, 6, 7, 8, 9] -> [[2, 3], [4, 5], [6, 7], [8, 9]]
    pass


# def test_pairs():
#     assert list(pairs([0, 1, 2, 3, 4, 5])) == [[0, 1], [2, 3], [4, 5]]
#     # Bonus
#     assert list(pairs([0, 1, 2, 3, 4])) == [[0, 1], [2, 3], [4]]


def blank_count(ol):
    # Count the amount of not True elements in ol
    pass


# def test_blank_count():
#     assert blank_count([7, 0, None, 1, 'hi', '', 88, 0]) == 4


def flatten(ol_of_ol):
    # For [[1, 2, 3], [4, 5, 6], [7, 8]] -> [1, 2, 3, 4, 5, 6, 7, 8]
    pass


# def test_flatten():
#     assert flatten([[1, 2, 3], [4, 5], [6, 7]]) == [1, 2, 3, 4, 5, 6, 7]


def element_divisible_by_3(ol):
    # Is there 1 or more elements divisible by 3 in the input
    pass


# def test_element_divisible_by_3():
#     assert element_divisible_by_3([1, 2, 4, 5]) == False
#     assert element_divisible_by_3([1, 2, 6, 5]) == True


def most_common(ol):
    # Return the most common element in the input list
    pass


# def test_most_common():
#     assert most_common([3, 3, 4, 4, 4, 4, 2]) == 4


def dict_reverse(d):
    # For {'a': 3, 'b': 4, 'c': 9} -> {3: 'a', 4: 'b', 9: 'c'}
    pass


# def test_dict_reverse():
#     assert dict_reverse({'a': 3, 'b': 4, 'c': 9}) == {3: 'a', 4: 'b', 9: 'c'}


def atomic_weight(formula):

    def weight(element='Na'):
        import mendeleev
        return getattr(mendeleev, element).atomic_weight

    pass


# def test_atomic_weight():
#     assert atomic_weight('NaCl')     == pytest.approx(58.4,  0.01)
#     assert atomic_weight('CCl4')     == pytest.approx(153.8, 0.01)
#     assert atomic_weight('H2O')      == pytest.approx(18.0,  0.01)
#     assert atomic_weight('H2SO4')    == pytest.approx(98.1,  0.01)
#     assert atomic_weight('C6H12COH') == pytest.approx(113.2, 0.01)


def sequences(max_len):
    '''
    For a given max_len return all combinations of ACGT, first of
    length 1, then 2, until max_len is reached
    eg.
        3 -> ['A', 'C', 'G', 'T', 'AC', 'AG', 'AT', 'CG', 'CT', 'GT', 'ACG',
              'ACT', 'AGT', 'CGT']
    '''
    pass


# def test_sequences():
#     assert list(sequences(3)) == ['A', 'C', 'G', 'T', 'AC', 'AG', 'AT', 'CG',
#                                   'CT', 'GT', 'ACG', 'ACT', 'AGT', 'CGT']


def stock_prices(ticker):
    prices = {
        '2019-02-14': {
            'MSFT':  106,
            'GOOG': 1120,
        },
        '2019-02-15': {
            'MSFT':  108,
            'NFLX':  351,
        },
        '2019-02-18': {
            'MSFT':  108,
            'GOOG': 1119,
            'NFLX':  352,
        },
        '2019-02-19': {
            'MSFT':  109,
            'GOOG': 1122,
            'NFLX':  107,
        },
    }


# def test_stock_prices():
#     assert set(stock_prices('MSFT')) == set([ 106,  108,  108,  109])
#     assert list(stock_prices('MSFT')) == [ 106,  108,  108,  109]
#     assert list(stock_prices('NFLX')) == [None,  351,  352,  107]
#     assert list(stock_prices('GOOG')) == [1120, 1120, 1119, 1122]


def main():
    import os
    filename = os.path.basename(__file__)
    pytest.main([filename])


if __name__ == '__main__':
    main()
