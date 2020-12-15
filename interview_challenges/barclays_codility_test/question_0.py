def solution(A):
    # write your code in Python 2.7
    result = []
    for i, _ in enumerate(A):
        before = A[:i]
        after  = A[i+1:]
        if sum(before) == sum(after):
            result.append(i)
    return result


def main():
    print solution([-1, 3, -4, 5, 1, -6, 2, 1])

if __name__ == '__main__':
    main()
