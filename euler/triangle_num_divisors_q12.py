import math
import time


def triangle(n):
    return int(n * (n + 1) / 2.0)


def divisors(n):
    lowers = [i for i in range(1, math.ceil(math.sqrt(n)) + 1) if n % i == 0]
    uppers = [int(n / low) for low in reversed(lowers)]
    return len(set(lowers + uppers))


def divisor_count(stop):
    i = 1
    while True:
        if divisors(triangle(i)) > stop:
            return i
        i = i + 1


def main():
    print(divisor_count(0), triangle(divisor_count(0)))   # expect  1
    print(divisor_count(1), triangle(divisor_count(1)))   # expect  2
    print(divisor_count(2), triangle(divisor_count(2)))   # expect  3
    print(divisor_count(3), triangle(divisor_count(3)))   # expect  3
    print(divisor_count(4), triangle(divisor_count(4)))   # expect  7

    print('Answer:', triangle(divisor_count(500)))


if __name__ == '__main__':
    main()
