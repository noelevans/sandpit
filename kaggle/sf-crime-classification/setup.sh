#!/bin/sh

wget --load-cookies=cookies.txt https://www.kaggle.com/c/sf-crime/download/test.csv.zip
wget --load-cookies=cookies.txt https://www.kaggle.com/c/sf-crime/download/train.csv.zip
wget --load-cookies=cookies.txt https://www.kaggle.com/c/sf-crime/download/sampleSubmission.csv.zip

unzip test.csv.zip
unzip train.csv.zip

# head -10 test.csv > test.small.csv
# head -10000 train.csv > train.small.csv

# grep ",INGLESIDE,\|,NORTHERN,\|DayOfWeek" train.csv > train.small.csv
# grep ",INGLESIDE,\|,NORTHERN,\|DayOfWeek" test.csv > test.small.csv
grep ",PARK,\|,RICHMOND,\|DayOfWeek" train.csv > train.small.csv
grep ",PARK,\|,RICHMOND,\|DayOfWeek" test.csv > test.small.csv
