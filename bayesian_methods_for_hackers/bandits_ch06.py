import numpy as np
from pymc import rbeta


class Bandits(object):
    """Class representing N bandits machines.

    Args:
        p_array ([floats]): a (N,) array of probabilities >0, <1
    """

    def __init__(self, p_array):
        self.p = p_array
        self.optimal = np.argmax(p_array)

    def pull(self, i):
        """Results in 0 or 1; pulling the ith bandit."""
        return np.random.rand() < self.p[i]

    def __len__(self):
        return len(self.p)


class BayesianStrategy(object):
    """Online, learning algorithm to solve the Multi-Armed Bandit problem.

        Args:
            bandits (Bandit): multi-armed bandit machine object

        N: Cumulative number of samples
        choices: Historical choices as a (N,) array
        bb_score: Historical score as a (N,) array
    """

    def __init__(self, bandits):
        self.bandits = bandits
        n_bandits = len(self.bandits)
        self.wins = np.zeros(n_bandits)
        self.trials = np.zeros(n_bandits)
        self.N = 0
        self.choices = []
        self.bb_score = []

    def sample_bandits(self, n=1):
        """Sample and train on n pulls"""
        bb_score = np.zeros(n)
        choices = np.zeros(n)

        for k in range(n):
            # sample from the bandits's priors, and select the largest sample
            choice = np.argmax(
                rbeta(1 + self.wins, 1 + self.trials - self.wins))

            # sample the chosen bandit
            result = self.bandits.pull(choice)

            # update priors and score
            self.wins[choice] += result
            self.trials[choice] += 1
            bb_score[k] = result
            choices[k] = choice

        self.N = n
        self.bb_score = np.r_[self.bb_score, bb_score]
        self.choices = np.r_[self.choices, choices]


def main():
    # Create 3 bandits - [best, worst, good_second_place]
    strat = BayesianStrategy(Bandits(np.array([0.30, 0.05, 0.25])))

    # Give the system 100,000 attempts to make as much money as possible
    strat.sample_bandits(100000)

    # Algo's estimation of bandits' yield rates. Accuracy will be worse for
    # weaker bandits - don't try them so much if you are sure they yield less
    print(strat.wins / strat.trials)

    # How many times each bandit has been pulled. It should have hammered the
    # best bandit many more times than the worst to optimise earnings
    print(strat.trials)
    print(strat.N)


if __name__ == '__main__':
    main()

