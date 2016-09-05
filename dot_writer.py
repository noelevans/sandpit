import os
import time
import numpy as np


def write_sample(filename):
    with open(filename, 'a') as f:
        f.write('.')


def main():
    commits = np.random.poisson(0.28)
    filename = 'sample_text.txt'

    for c in range(commits):
        write_sample()
        timestamp = str(time.time()).replace('.', '')
        args = (filename, timestamp)
        os.system('git commit %s -m "Add sample text: %s"' % args)
        time.sleep(np.random.rand())

    os.system('git push')


if __name__ == '__main__':
    main()
