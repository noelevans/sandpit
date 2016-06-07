import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


""" Fluctuations of AAPL price, analysing quantiles to see for "random" data,
    how many data points are flagged as outliers for 10% quantile increments.
"""

DATA = """2016-06-01,98.46
            2016-05-31,  99.86
            2016-05-27, 100.35
            2016-05-26, 100.41
            2016-05-25,  99.62
            2016-05-24,  97.90
            2016-05-23,  96.43
            2016-05-20,  95.22
            2016-05-19,  94.20
            2016-05-18,  94.56
            2016-05-17,  93.49
            2016-05-16,  93.88
            2016-05-13,  90.52
            2016-05-12,  90.34
            2016-05-11,  92.51
            2016-05-10,  93.42
            2016-05-09,  92.79
            2016-05-06,  92.72
            2016-05-05,  93.24
            2016-05-04,  94.19
            2016-05-03,  95.18
            2016-05-02,  93.64
            2016-04-29,  93.74
            2016-04-28,  94.83
            2016-04-27,  97.82
            2016-04-26, 104.35
            2016-04-25, 105.08
            2016-04-22, 105.68
            2016-04-21, 105.97
            2016-04-20, 107.13
            2016-04-19, 106.91
            2016-04-18, 107.48
            2016-04-15, 109.85
            2016-04-14, 112.10
            2016-04-13, 112.04
            2016-04-12, 110.44
            2016-04-11, 109.02
            2016-04-08, 108.66
            2016-04-07, 108.54
            2016-04-06, 110.96
            2016-04-05, 109.81
            2016-04-04, 111.12
            2016-04-01, 109.99
            2016-03-31, 108.99
            2016-03-30, 109.56
            2016-03-29, 107.68
            2016-03-28, 105.19
            2016-03-24, 105.67
            2016-03-23, 106.13
            2016-03-22, 106.72
            2016-03-21, 105.91
            2016-03-18, 105.92
            2016-03-17, 105.80
            2016-03-16, 105.97
            2016-03-15, 104.58
            2016-03-14, 102.52
            2016-03-11, 102.26
            2016-03-10, 101.17
            2016-03-09, 101.12
            2016-03-08, 101.03
            2016-03-07, 101.87
            2016-03-04, 103.01
            2016-03-03, 101.50
            2016-03-02, 100.75
            2016-03-01, 100.53
            2016-02-29,  96.69""".split('\n')

def main():
    to_date = lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date()
    to_date_and_price = lambda d, p: (to_date(d), float(p))

    pair_data = [to_date_and_price(*(d.strip().split(','))) for d in DATA]
    data = [{'date': d[0], 'price': d[1]} for d in pair_data]
    df = pd.DataFrame(data, columns=['date', 'price'])
    quantiles = df.quantile(np.arange(0, 1, 0.1)[1:]).price.tolist()

    plot_ = df.plot(color='b')

    plot_.set_axis_bgcolor('IndianRed')
    # alpha = 0.799
    alpha = 0.0
    for n, (q, q_1) in enumerate(zip(quantiles, reversed(quantiles))):
        if n < len(quantiles) / 2.0:
            print(alpha)
            plot_.barh(q, len(df.date), q_1-q, color='white', alpha=alpha)
            alpha += 0.2

    plt.show()


if __name__ == '__main__':
    main()
