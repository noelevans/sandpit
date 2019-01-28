"""
    To be used with ipython when it starts up. Create a sym-link to this file in
    the default ipython profile like so:
        ln -s ~/repo/sandpit/start_ipython.py
                ~/.ipython/profile_default/startup/start_ipython.py
"""

import datetime
import decimal
import itertools
import json
import math
import matplotlib
import operator
import random
import re
import time
import timeit

# import matplotlib.pyplot as plt    # very slow
import numpy as np
import pandas as pd
# import pymc as pm
import scipy as sp

from collections import Counter
from pprint import pprint as pp
from sklearn import datasets
from scipy import stats

from IPython.core.pylabtools import figsize


pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 100)


def describe(ol):
    print(df.Series(ol).describe())


def nCr(n, r):
    return sp.misc.comb(n, r, exact=True)


def exp_decay(days, half_life=0.05):
    return half_life ** (days / 30.0)


# matplotlibrc_path = '/home/noel/repo/sandpit/matplotlibrc.json'
# matplotlib.rcParams.update(json.load(open(matplotlibrc_path)))

today = lambda: datetime.date.today()
tomorrow = lambda: today() + datetime.timedelta(days=1)
yesterday = lambda: today() - datetime.timedelta(days=1)

data = [{'num': 2, 'date': yesterday()},
        {'num': 3, 'date': today()},
        {'num': 4, 'date': tomorrow()}]
df_small = pd.DataFrame(data, columns=['num', 'date'])
df = df_small
