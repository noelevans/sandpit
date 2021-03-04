import random
import pytest

"""
You have a list of 10M values. You want to order all the values to get the
5% value (for something like 2 std deviations). This pivoting performs 
at O(2n) rather n.log(n) when sorting the whole array.

It's also better for memory use.
"""


def get(ul, k):
    pivot = ul[0]
    tail = ul[1:]
    fore = []
    aft = []
    for el in tail:
        if el < pivot:
            fore.append(el)
        else:
            aft.append(el)
    if k < len(fore):
        return get(fore, k, 0)
    elif k == len(fore):
        return pivot
    else:
        return get(aft, k - len(fore) - 1)


@pytest.mark.parametrize("arg, expected", [(5, 106), (95, 196)])
def test_kth_element(arg, expected):
    ul = list(range(101, 201))
    random.seed(0)
    random.shuffle(ul)
    assert get(ul, arg) == expected
