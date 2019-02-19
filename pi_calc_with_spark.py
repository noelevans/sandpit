import pyspark
import random


"""
Run with
    $ SPARK_HOME/bin/spark-submit pi_calc_with_spark.py

"""


def inside(rdd):
    x, y = random.random(), random.random()
    return x*x + y*y < 1


def main():
    samples = 100000000     # Too much for my laptop to act as cluster, so:
    samples = 10000000

    with pyspark.SparkContext('local') as sc:
        count = sc.parallelize(range(samples)).filter(inside).count()
        pi = 4.0 * count / samples
    print('Pi is roughly...........................', pi)

    # or locally ...
    (np.square(np.random.random((samples, 2))).sum(1) < 1).sum() * 4 / samples

if __name__ == '__main__':
    main()
