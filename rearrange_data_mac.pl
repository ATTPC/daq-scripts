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
use File::Copy "mv";

my $usage = "This script rearranges and renames the fetched data files.\n"
              . "Please provide an experiment name as the first argument.\n";

if (@ARGV == 0) {
  print $usage and exit 1;
}

my $expname = $ARGV[0];

# Change these paths to change where to find and put the files

my $fetchdir = "/data/$expname/temp";
my $cleandir = "/data/$expname";

# Now, do the rearranging

print "Rearranging files for experiment $expname \n";

for my $n (0 .. 9) {
  # This is looping over the mmN folders for the mac minis 
  print "Entering directory for mm$n \n";
  if ( chdir("$fetchdir/mm$n") ) {
    # chdir returns true if successful, meaning the folder exists
    opendir(DIR, "."); 
    my @files = grep(/dat/,readdir(DIR));  # list the files
    for my $file (@files) {
      $file =~ /(run_\d\d\d\d)(\.dat\.)(.*)/;  # match "run_XXXX.dat.(timestamp)"
      my $newFileName = "CoBo$n\_$1_$3.graw";  # output as "CoBoX_run_XXXX_(timestamp).graw"
      my $rundir = $1;
      if (not -d "$cleandir/$rundir" ) {
        make_path("$cleandir/$rundir");  
      }
      mv($file,"$cleandir/$rundir/$newFileName") if not -e "$cleandir/$rundir/$newFileName";
    }
  }
}
