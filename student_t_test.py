from scipy.stats import ttest_ind   # Frequentist
from scipy.stats import f_oneway    # Bayesian


def main():
    # run_times_before = [30.02, 29.99, 30.11, 29.97, 30.01, 29.99]
    run_times_before = [31.02, 31.00, 31.01, 31.03, 31.01, 31.00]
    run_times_after  = [29.89, 29.93, 29.72, 29.98, 30.02, 29.98]

    t_freq, p_freq = ttest_ind(run_times_before, run_times_after)
    t_bayes, p_bayes = f_oneway(run_times_before, run_times_after)
    print('Frequentist p_value: %.12e' % p_freq)
    print('Bayesian p_value:    %.12e' % p_bayes)


if __name__ == '__main__':
    main()
