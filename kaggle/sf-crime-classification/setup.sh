#!/bin/sh

wget https://www.kaggle.com/c/sf-crime/download/test.csv.zip
wget https://www.kaggle.com/c/sf-crime/download/train.csv.zip

unzip test.csv.zip
unzip train.csv.zip

rm test.csv.zip train.csv.zip

