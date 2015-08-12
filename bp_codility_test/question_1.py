import itertools


def solution(N):
    # write your code in Python 2.7
    nums = [int(v) for v in str(N)]
    return len(set(itertools.permutations(nums)))


def main():
    print solution(1213)
    print solution(0)
    print solution(99999)

if __name__ == '__main__':
    main()
