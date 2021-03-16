import random
import pytest
import statistics
import time

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
        return get(fore, k)
    elif k == len(fore):
        return pivot
    else:
        return get(aft, k - len(fore) - 1)


def _sorted(ul):
    if not ul:
        return []
    return (
        _sorted([el for el in ul[1:] if el < ul[0]])
        + [ul[0]]
        + _sorted([el for el in ul[1:] if el >= ul[0]])
    )


def c_traditional_get(ul, k):
    ol = _sorted(ul)
    return ol[k]


def native_traditional_get(ul, k):
    ol = _sorted(ul)
    return ol[k]


@pytest.mark.parametrize("arg, expected", [(5, 106), (95, 196)])
def test_kth_element(arg, expected):
    ul = list(range(101, 201))
    random.seed(0)
    random.shuffle(ul)
    assert get(ul, arg) == expected


if __name__ == "__main__":

    def _timer(fn, ul):
        index = len(ul) // 2
        start = time.time()
        _ = fn(ul, index)
        return time.time() - start

    for e in range(1, 8):
        n = 10 ** e
        ul = list(range(10 ** e))
        random.shuffle(ul)

        two_n = _timer(get, ul)
        native = _timer(native_traditional_get, ul)
        c_native = _timer(c_traditional_get, ul)
        stats_lib = _timer(lambda the_ul, x: statistics.median(the_ul), ul)
        print(
            f"For {len(ul)} records: 2n = {two_n}, native = {native}, c_native = {c_native}, stats_lib = {stats_lib}"
        )
