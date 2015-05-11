#!/bin/sh

ITERATIONS=`python -c 'import numpy; print numpy.random.poisson(0.5)'`
echo $ITERATIONS

(cd all && seq $ITERATIONS | xargs -I INDEX git pull)
