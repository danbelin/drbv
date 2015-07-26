#!/usr/bin/perl

#check for arguments
if($#ARGV + 1 != 1) {
    print "\nUsage: cleaner.pl [filename]\n";
    exit; 
}

$filename=$ARGV[0];

open(FILEDATA, $filename) or die "File IO Error on file $filename";

while(<FILEDATA>){
    ProcessLine($_);
}

sub ProcessLine{
    my $line = shift;
    #clean trailing and leading whitespace
    $line =~ s/^\s+|^\t+//;
    $line =~ s/\s+$|\t+$//;
    
    #initial delimiter
    $line =~  s/\h+/,/g;
    
    #clean up the research type field which gets maligned
    my ($researchtype) = $line =~ /^.*\d+(.*?)$/;
    $researchtype =~ s/(.*?)\,//;
    (my $correctedresearchtype = $researchtype) =~ s/\,/ /g;
    
    #clean up the line item name which is similarly maligned
    my ($itemname) = $line =~ /\,(.*)/;
    $itemname =~ s/(.*?)\,//;
    $itemname =~ s/(?<=\,)\d(?=\d)(.*)//;
    (my $correcteditemname = $itemname) =~ s/\,(?=.*\,)/ /g;

    #final correction
    $line =~ s/\Q$researchtype\E(?!.*\Q$researchtype\E)/$correctedresearchtype/;
    $line =~ s/\Q$itemname\E/$correcteditemname/;
    
    print "$line\n";
    return $line; 
}
