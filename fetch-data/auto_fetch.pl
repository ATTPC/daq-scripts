#!/usr/bin/perl

use warnings;
use strict;

if (@ARGV == 0) {
	print "Please provide an experiment name, configuration name, and run name as an argument.\n" and exit 1;
}

my $expname = $ARGV[0]; # i.e. alphas
#my $cfgname = $ARGV[1]; # i.e. nobeam, pedestals
my $runnum  = $ARGV[1]; # i.e. run_0020

#my $cfgfilename = "/daq/Configs/configure-$cfgname-all.xcfg";
#if not -e $cfgfilename {
#	print "File $cfgfilename does not exist.\n Did you provide a valid configuration name?\n" and exit 2;
#}
#my $cfgfilename_new = "/data/cleaned/$expname/$runnum/configure-$cfgname-all.xcfg";

print "Fetching and rearranging data for experiment $expname.\n";

my $ansible_cmd = "ansible-playbook /Users/attpc/ansible-attpc/fetch-data/fetch-file.yml --extra-vars 'exp_name=$expname run_name=$runnum'";
my @rearrange_cmd = ("/Users/attpc/ansible-attpc/rearrange_data_mac.pl","$expname");

# print "$ansible_cmd\n";
# print "@rearrange_cmd\n";

system($ansible_cmd);
system(@rearrange_cmd);

print "Finished fetching data.\n"

#system(cp,$cfgfilename,$cfgfilename_new);
