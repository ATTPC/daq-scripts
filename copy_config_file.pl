#!/usr/bin/perl

use strict;
use warnings;

use File::Copy "cp";

if (@ARGV < 2)
{
	print "Please provide a configuration and run name:\n i.e. nobeam run_0012\n" and exit 1;
}

my $config_name = $ARGV[0];
my $run_name = $ARGV[1];

my $cleandir = "/data/cleaned/alphas/configs_used";

my $cfg_src = "/daq/Configs/configure-$config_name-all.xcfg";
if (not -e $cfg_src)
{
	print "Configuration file not found.\n" and exit 2;
}

my $cfg_dest = "$cleandir/configure-$config_name-all-$run_name.xcfg";

cp($cfg_src,$cfg_dest) or die "File copy failed.";
