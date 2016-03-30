import collections


class SomeFibonacci(object):

    def __init__(self):
        self.fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

    def __getitem__(self, ns):
        if isinstance(ns, collections.Iterable):
            return [f for n, f in enumerate(self.fibs) if n in ns]
        else:
            return self.fibs[ns]


def main():
    fibs = SomeFibonacci ()
    print(fibs[2])
    print(fibs[5])
    print(fibs[2, 5])


if __name__ == '__main__':
    main()
