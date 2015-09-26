import numpy as np
import string
import time


"""
Winning submission for team (~35 ppl) competition to build an internal table
similar to pandas.DataFrame using random numbers and letters to fill each cell
with n chars in quickest time possible.

Required format to pass to table cons: (data, column_names):

    np.array([['ab','cd'],['ef','gh'],['ij','kl']]),
    ['one', 'two']

"""

POS_MAP = np.array(list(string.ascii_letters + string.digits))
CHAR_LEN = len(string.ascii_letters + string.digits)


def make(n=3, ord=3, cols=10):
    """ Generate random chars in a QzTable
        n:    characters per cell
        ord:  row count = 10^ord
        cols: column count
    """
    points = n * cols * (10 ** ord) + (cols * n)
    data_indicies = np.random.randint(CHAR_LEN, size=points)
    raw_data = POS_MAP[data_indicies]
    cells = raw_data.view('S%i' % n)
    arr = np.array(cells).reshape(len(cells) / cols, cols)
    return table.np_table(arr[1:], colNames=list(arr[0]))


def profile(f):
    import cProfile, pstats, StringIO
    pr = cProfile.Profile()
    pr.enable()
    f(n=5, ord=6, cols=3)
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'time'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()


def measure(f):
    f(n=2, ord=2)  # Warm things up a bit
    def _measure(n, ord, cols):
        before = time.time()
        out = f(n=n, ord=ord, cols=cols)
        after = time.time()
        print "%s: %.2f s" % (f, after - before)
    _measure(2, 3, 2)
    _measure(2, 5, 2)
    _measure(5, 5, 10)
    _measure(100, 4, 2)


def main():
    # t = time.time()
    # _ = make(5, 6, 10)
    # print 'Result:', time.time() - t
    # print make(4, 1, 3)
    measure(make)
    profile(make)


if __name__ == '__main__':
    main()
