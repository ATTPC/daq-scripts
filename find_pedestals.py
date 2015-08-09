#!/usr/bin/env python3

import pytpc
import pandas as pd
import os
import sys

import argparse
from clint.textui import progress, puts, indent

from time import sleep


def calculate_pedestals(evt, min_tb, max_tb):
	"""Calculate the pedestals by averaging the traces between `min_tb` and `max_tb`.

	Parameters
	----------
	evt : pytpc.Event
		The event to find pedestals for.
	min_tb, max_tb : integer
		The bounds on the mean. Each trace will be averaged over the slice `min_tb:max_tb`.

	Returns
	-------
	pandas.Series
		The pedestals as floats, indexed by pad number.
	"""

	assert 0 <= min_tb < max_tb < 512, 'invalid time bucket range'

	peds = evt.traces['data'][:, min_tb:max_tb].mean(1)
	pads = evt.traces['pad']

	return pd.Series(peds, index=pads, name='ped')


def main():

	# Parse command line arguments

	parser = argparse.ArgumentParser(description='A script for finding the pedestals from a baseline run.')
	parser.add_argument('input', type=str,
						help='Path to an event file')
	parser.add_argument('output', type=str,
						help='Where to put the table of pedestals')
	parser.add_argument('--evt-range', '-e', type=int, nargs=2, metavar=('MIN_EVT', 'MAX_EVT'),
						help='Range of events to consider (default: all in file)')
	parser.add_argument('--data-range', '-d', type=int, nargs=2, metavar=('MIN_TB', 'MAX_TB'),
						help='Range of timestamps to average over (default: 0 to 511)')
	args = parser.parse_args()

	# Open the file

	efile = pytpc.EventFile(args.input)

	# Interpret the bounds for the pedestal calculation

	if args.evt_range is not None:
		min_evt, max_evt = args.evt_range
	else:
		min_evt, max_evt = 0, len(efile)

	if not (0 <= min_evt < max_evt):
		sys.exit('Error: Min evt must be less than max evt, and both must be >= 0')

	if args.data_range is not None:
		min_tb, max_tb = args.data_range
	else:
		min_tb, max_tb = 0, 511

	if not(0 <= min_tb < max_tb < 512):
		sys.exit('Error: Data range (in time buckets) is from [0,511], and must have min < max.')

	# Create a table to hold the pedestals

	ped_table = pd.DataFrame(index=range(10240), columns=('cobo', 'asad', 'aget', 'channel', 'ped'))
	ped_table.index.name = 'pad'

	# Find cobo, asad, etc. for each pad from the first event

	print('\nRecovering pad mapping from first event in file...')

	evt = efile[0]
	ped_table.loc[evt.traces['pad'], ['cobo', 'asad', 'aget', 'channel']] = evt.traces[['cobo', 'asad',
																						'aget', 'channel']].view('u1').reshape(-1, 4)
	del evt

	ped_table.loc[ped_table.cobo.notnull(), 'ped'] = 0  # initialize peds to zero for all non-null pads

	print('Done!\n')

	# Now find the pedestals for each event

	for i in progress.bar(range(min_evt, max_evt), label='Processing events '):
		evt = efile[i]
		ped_table.loc[:, 'ped'] += calculate_pedestals(evt, min_tb, max_tb)

	ped_table.loc[:, 'ped'] /= (max_evt - min_evt)  # divide by the number of events to find the mean

	# Save the output

	ped_table.to_csv(args.output)

	print('Wrote pedestals to file', args.output)

if __name__ == '__main__':
	main()
