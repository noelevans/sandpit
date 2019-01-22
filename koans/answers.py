import collections
import itertools
import math
import mendeleev
import re


def my_range():
    return list(range(1, 10+1))


def average(ol):
    return sum(ol) / len(ol)


def no_whitespace(t):
    return t.strip()


def minus_to_plus(t):
    return t.replace('-', '+')


def sum_bar_last(*args):
    return sum(args[:-1]) - args[-1]


def mirror(ol):
    return ol[::-1]


def odd_idxs(ol):
    return list(ol[::2])


def pairs(ol):
    return list(zip(ol[::2], ol[1::2]))


def blank_count(ol):
    return len([el for el in ol if not el])


def flatten(ol_of_ol):
    # result = []
    # for ol in ol_of_ol:
    #     result.extend(ol)
    # return result

    return list(itertools.chain.from_iterable(ol_of_ol))


def element_divisible_by_3(ol):
    return any(x for x in ol if x % 3 == 0)


def most_common(ol):
    return collections.Counter(ol).most_common(1)[0][0]


def dict_reverse(d):
    return {v: k for k, v in d.items()}


def sequences(max_len):
    for n in range(1, max_len+1):
        for el in itertools.combinations('ACGT', n):
            yield el


def weight(formula):
    chunks = re.findall('([A-Z][a-z]*|[0-9]+)', formula)
    total = 0
    while chunks:
        element = chunks.pop(0)
        if chunks and chunks[0].isnumeric():
            count = int(chunks[0])
            chunks.pop(0)
        else:
            count = 1
        element_weight = getattr(mendeleev, element).atomic_weight * count
        total = total + element_weight

    return total


def main():
    print(my_range())
    print(average([2, 3, 4]))
    print(no_whitespace('   hello    '))
    print(minus_to_plus('hello-world'))
    print(sum_bar_last(2, 3, 4))
    print(mirror('Hello'))
    print(odd_idxs(range(20)))
    print(pairs(range(20)))
    print(blank_count([7, 0, None, 1, 'hi', '', 88, 0]))
    print(flatten([(1, 2), (3, 4), (5, 6)]))
    print(element_divisible_by_3([1, 2, 4, 5]))
    print(element_divisible_by_3([1, 2, 3, 5]))
    print(most_common([3, 3, 4, 4, 4, 4, 2]))
    print(dict_reverse({'a': 2, 'b': 7}))
    print(list(sequences(3)))
    print('')
    print(weight('NaCl'))
    print(weight('CCl4'))
    print(weight('H2O'))
    print(weight('H2SO4'))
    print(weight('C6H12COH'))


if __name__ == '__main__':
    main()
