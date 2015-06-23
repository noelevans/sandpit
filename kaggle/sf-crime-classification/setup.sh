#!/bin/sh

unzip test.csv.zip
unzip train.csv.zip

head -10 test.csv > test.small.csv
head -10000 train.csv > train.small.csv
