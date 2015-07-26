#!/usr/bin/perl

#check for arguments
if($#ARGV + 1 != 1) {
    print "\nUsage: postclean.pl [filename]\n";
    exit; 
}

$filename=$ARGV[0];

open(FILEDATA, $filename) or die "File IO Error on file $filename";

while(<FILEDATA>){
    ProcessLine($_);
}

sub ProcessLine{
    my $line = shift;
    my @columns = split /\,/, $line;
    my @FY14columns = ($columns[0], $columns[1], $columns[2], $columns[3], $columns[$#columns-1], $columns[$#columns]);
    
    print join(",", @FY14columns);    
}
