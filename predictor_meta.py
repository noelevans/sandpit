from sklearn import datasets

"""
Examples to classify:
    Names (Unique / MostlyUnique)
    Cost (Unique / MostlyUnique)
    Is by river (Categorical)
    PKs (Unique)
    Title: Mr, Dr, Mrs,... (Categorical)
    Ticket cost

"""

class DTypes:
    Unique = 0
    MostlyUnique = 1
    Categorical = 2


def likely_unique(ol):
    uniques = len(set(ol))
    _, p_test = f_oneway(
        [True] * len(ol),
        [False] * (len(ol) - uniques) + [True] * uniques)
    return p_test > 0.05


def likely_categorical(ol):
    uniques = len(set(ol))
    len(ol)

def main():
    data = datasets.load_boston().data
    for d in data.T:
        print(len(d))
        print(len(set(d)))
        print(d[0])
        break


if __name__ == '__main__':
    main()
