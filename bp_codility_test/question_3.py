import itertools


def do_output(b, r, g, A):
    result = []
    for a in A:
        if a in b:
            result.append('B')
        if a in r:
            result.append('R')
        if a in g:
            result.append('G')
    return ''.join(result)


def solution(A):
    _all = set(A)

    for b in reversed(range(len(A) + 1)):
        b_combs = [set(x) for x in itertools.combinations(A, b)]
        for b_comb in b_combs:
            remain_vals = _all - b_comb
            for r in reversed(range(len(remain_vals) + 1)):
                r_combs = [set(x) for x in itertools.combinations(remain_vals, r)]
                for r_comb in r_combs:
                    g_comb = _all - b_comb - r_comb
                    
                    if sum(b_comb) == sum(r_comb) == sum(g_comb):
                        return do_output(b_comb, r_comb, g_comb, A)

    return 'impossible'


def main():
    print solution([3, 7, 2, 5, 4])
    print solution([3, 6, 9])


if __name__ == '__main__':
    main()
