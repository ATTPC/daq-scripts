#!/usr/bin/perl

# rearrange_data.pl
# -----------------
# This script will look for the data files fetched from the daq nodes and 
# rearrange them into a more sensible directory tree. The path variables
# may need to be changed if configurations are changed in the system.
#
# This script is NOT COMPLETE as of 8/15/2014 (JWB)


use warnings;
use strict;
use Cwd;
use File::Path qw(make_path);
use File::Copy "cp";

if (@ARGV == 0) {
  print "No directory given in the arugments.\n" and die;
}

my $expname = $ARGV[0];
my $fetchdir = "/data/fetched";
my $cleandir = "/data/cleaned";

my $subpath = "ganacq_manip/$expname/acquisition/run";
my $finalpath = "$cleandir/$expname";

my @mmx = ("mm0","mm1","mm2","mm3","mm4","mm5","mm6","mm7","mm8","mm9");

print "Rearranging files for experiment $expname \n";

make_path($finalpath);

for my $mmn (@mmx) {
  print "Entering directory for $mmn";
  chdir("$fetchdir/$mmn/$subpath") or die "Chdir failed: $!";
  opendir(DIR, ".");
  my @files = grep(/dat/,readdir(DIR));
  for my $file (@files) {
    print $file;
  }
}
