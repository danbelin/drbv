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
    $columns[5] =~ s/ //g;
    print join(",", @columns);    
}
