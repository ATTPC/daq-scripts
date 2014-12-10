#!/usr/bin/perl

use warnings;
use strict;

if (@ARGV == 0) {
	print "Please provide an experiment name as an argument.\n" and exit 1;
}

my $expname = $ARGV[0];

print "Fetching and rearranging data for experiment $expname.\n";

my @ansible_cmd = ("ansible-playbook","/home/attpc/ansible-attpc/fetch-data/fetch.yml");
my @rearrange_cmd = ("/home/attpc/ansible-attpc/rearrange_data.pl","$expname");

system(@ansible_cmd);
system(@rearrange_cmd);
