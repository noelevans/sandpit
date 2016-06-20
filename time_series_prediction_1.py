import datetime
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


DATA = [1807, 1957, 1574, 1531, 1026, 973, 1207, 1127, 1171, 811, 21534, 28001,
        40021, 27690, 20560, 17119, 16904, 22417, 9585, 25978, 26957, 14802,
        10794, 13838, 22581, 14669, 3684, 10126, 13599, 27646, 17838, 17028,
        14616, 14433, 27013, 11949, 42065, 9907, 9951, 22854, 12362, 10369,
        10833, 13040, 21326, 15637, 6846, 7070, 10412, 21954, 12614, 24361,
        13038, 12850, 30691, 21348, 11775, 12354, 12098, 24439, 14209, 9804,
        9589, 10614, 21312, 11933, 10310, 10138, 19546, 24428, 22483, 10746,
        13125, 13556, 25044, 9880, 16182, 13138, 25781, 25709, 14522, 8779,
        9969, 9779, 21988, 13763, 9075, 9544, 11393, 21210, 10454, 4307, 4456,
        8944, 18892, 9262, 13495, 8258, 7197, 21006, 18046, 4002, 11867, 8192,
        21920, 9979, 4031, 4840, 4820, 16573, 6917, 4084, 5296, 4821, 19136,
        15487, 6127, 9275, 12540, 20698, 9229, 2389, 6735, 6563, 19895]


def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def main():
    start = datetime.date(2015, 9, 12)
    data = [{'date': start + datetime.timedelta(days=n), 'vol': val}
            for n, val in enumerate(DATA)]
    df = pd.DataFrame(data, columns=['date', 'vol'])
    mean = np.mean(df.vol)
    std = np.std(df.vol)
    lower_pc = np.percentile(df.vol,  2.5)
    upper_pc = np.percentile(df.vol, 97.5)

    f, (ax1, ax2) = plt.subplots(2)
    df.plot(ax=ax1)

    window_len = 20
    window = rolling_window(df.vol.values, window_len)
    rolling_lower_pc = np.percentile(window,  5, axis=1)
    rolling_upper_pc = np.percentile(window, 95, axis=1)
    X = np.arange(len(rolling_lower_pc)) + window_len
    ax1.fill_between(X, rolling_lower_pc, rolling_upper_pc, alpha=0.2)

    ax2.hist(df.vol, 20, alpha=0.7)
    ax2.axvspan(mean - 2 * std,
                mean + 2 * std,
                alpha=0.2,
                label='SD',
                zorder=-1)
    ax2.axvspan(lower_pc,
                upper_pc,
                alpha=0.4,
                color='grey',
                hatch='/',
                label='Percentiles',
                zorder=-1)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
