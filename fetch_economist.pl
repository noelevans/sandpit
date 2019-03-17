#!/usr/bin/perl

use strict;
use warnings;

# Run in cron with the appropriate directory set:
# cd /home/noel/tmp/books && ./fetch_economist.pl


# system 'wget https://raw.githubusercontent.com/kovidgoyal/calibre/master/recipes/economist.recipe';

# $output = `ebook-convert economist.recipe economist.mobi`;
my $filename = "output.txt";

my @output = (
    'This thing',
    'That 2019/03/14 thing',
);

# Read the mobi. Is it the new one?

# /2019/03/14/ 18
# /2019/03/16/ 68
my $date_match = "/([0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9])/";

while(my $line = <@output>)  {   

    if($line =~ m/(\d\d\d\d\/\d\d\/\d\d)/) { 
    	print "--Yes--$1\n"; 
    }    
}



# calibre-smtp -a economist.mobi -u SENDERNAME@PROVIDER.com -p PASSWORD -r smtp.PROVIDER.com --port 587 SENDERNAME@PROVIDER.com USERNAME@free.kindle.com ''
