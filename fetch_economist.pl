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
    'This 2019/03/16 thing',
    'This 2019/03/16 thing',
    'That 2019/03/14 thing',
);

# Read the mobi. Is it the new one?

# /2019/03/14/ 18
# /2019/03/16/ 68

my @dates;

while(my $line = <@output>)  {   

    if($line =~ m/(\d\d\d\d\/\d\d\/\d\d)/) { 
    	push @dates, $1; 
    }    
}

my %count; 
foreach my $value (@dates) {     
	$count{$value}++; 
} 

my $probable_date = ((sort {$count{$a} <=> $count{$b}} keys %count)[0]);
print $probable_date;
print "\n";


# calibre-smtp -a economist.mobi -u SENDERNAME@PROVIDER.com -p PASSWORD -r smtp.PROVIDER.com --port 587 SENDERNAME@PROVIDER.com USERNAME@free.kindle.com ''
