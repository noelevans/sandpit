#!/bin/sh

cd /var/www/html/lalaynbaluch/wp-content/themes/gridbox/

grep -rl 4477aa * | xargs echo sed -i 's/4477aa/new/g'
