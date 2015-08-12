# import numpy as np

def mean(ol):
    return float(sum(ol)) / len(ol)


def abs(v):
    return v > 0 and v or v * -1


def solution(A):    
    if not A:
        return -1

    m = mean(A)
    vs = sorted((abs(v - m), i) for i, v in enumerate(A))
    return vs[-1][1]


def main():
    print solution([])
    print solution([9, 4, -3, -10])
    print solution([-1, -20, -1, -1, -1])
    print solution([1, 1])
    print solution([1])


if __name__ == '__main__':
    main()
