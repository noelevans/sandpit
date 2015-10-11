results = {}


def next(v):
    return v % 2 == 0 and v // 2 or 3 * v + 1


def collatz_seq(n):
    v = n
    res = [n]
    while v != 1:
        v = next(v)
        res.append(v)
        if v in results:
            res.extend(results[v][1:])
            break
    results[n] = res
    return res


def main():
    N = 1000000
    print(max([(len(collatz_seq(n)), n) for n in range(1, N+1)]))


if __name__ == '__main__':
    main()
