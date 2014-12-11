#!/usr/bin/perl

# File:   rearrange_data.pl
# Author: Joshua Bradt
# -------------------------
# This script will look for the data files fetched from the daq nodes and 
# rearrange them into a more sensible directory tree. The path variables
# may need to be changed if configurations are changed in the system.

use warnings;
use strict;
use Cwd;
use File::Path qw(make_path);
use File::Copy "cp";

# Change these paths to change where to find and put the files

my $fetchdir = "/data/fetched";
my $cleandir = "/data/cleaned";

my $usage = "This script rearranges and renames the fetched data files.\n"
              . "Please provide an experiment name as the first argument.\n"
              . "I'll look for data in $fetchdir/[exp_name] and\n"
              . "I'll put it in $cleandir/[exp_name]/run_XXXX\n" ;

if (@ARGV == 0) {
  print $usage and exit 1;
}

my $expname = $ARGV[0];

# The next path is the subpath of $fetchdir where the files are found

# my $subpath = "ganacq_manip/$expname/acquisition/run";
my $subpath = "attpcX/$expname/acquisition/run";

my $finalpath = "$cleandir/$expname";

# Now, do the rearranging

print "Rearranging files for experiment $expname \n";

make_path($finalpath);

for my $n (0 .. 9) {
  # This is looping over the mmN folders for the mac minis 
  print "Entering directory for mm$n \n";
  if ( chdir("$fetchdir/mm$n/$subpath") ) {
    # chdir returns true if successful, meaning the folder exists
    opendir(DIR, "."); 
    my @files = grep(/dat/,readdir(DIR));  # list the files
    for my $file (@files) {
      $file =~ /(run_\d\d\d\d)(\.dat\.)(.*)/;  # match "run_XXXX.dat.(timestamp)"
      my $newFileName = "CoBo$n\_$1_$3.graw";  # output as "CoBoX_run_XXXX_(timestamp).graw"
      my $rundir = $1;
      if (not -d "$finalpath/$rundir" ) {
        make_path("$finalpath/$rundir");  
      }
      print "$file\n";
      #cp($file,"$finalpath/$rundir/$newFileName") if not -e "$finalpath/$rundir/$newFileName";
      if ((not -e "$finalpath/$rundir/$newFileName") and (not -l "$finalpath/$rundir/$newFileName")) {
        system("ln","-s","$fetchdir/mm$n/$subpath/$file","$finalpath/$rundir/$newFileName"); #or die "Died at file $file from mm$n.\n Return code was $?.";
      }
    }
  }
}
