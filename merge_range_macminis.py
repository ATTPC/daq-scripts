#!/usr/bin/env python3

import os
import sys
import subprocess
import json
import glob
import socket
import re

srcrt = '/data/attpcX/ar40/acquisition/run'
dstrt = '/data/merged/ar40'

lookup_path = os.path.expanduser('~/Lookup20150611.csv')
peds_path = os.path.expanduser('~/Pedestals20150810.csv')
threshold = '20'

results_path = os.path.join(dstrt, 'results.json')

cmd = ['pymerge', '-l', lookup_path, '-p', peds_path, '-t', threshold]

hostname = socket.gethostname()
mmn = int(re.match(r'mm(\d).*', hostname).group(1))

def path_string(lb, ub):
	n = lb
	while n <= ub:
		yield 'run_{:0>4}'.format(n)
		n += 1

def main():
	if len(sys.argv) < 3:
		print("Give lower / upper bounds.")
		return 1

	bounds = [ int(x) for x in sys.argv[1:] ]
	assert(len(bounds) == 2)
	lower_bound, upper_bound = min(bounds), max(bounds)

	if os.path.exists(results_path):
		f = open(results_path, 'r')
		results = json.load(f)
		f.close()
	else:
		results = {}

	for s in path_string(lower_bound, upper_bound):
		src_files = set(glob.glob(os.path.join(srcrt, s + '*')))
		lookup_files = set(glob.glob(os.path.join(srcrt, s + '*.lookup')))
		src_files -= lookup_files
		dst_path = os.path.join(dstrt, '{}_cobo{}.evt'.format(s, mmn))

		if len(src_files) == 0:
			print("The run {} does not exist.".format(s))
			print(39 * '-')
			continue

		this_cmd = cmd + src_files
		this_cmd.append('-o')
		this_cmd.append(dst_path)

		print("Running command:")
		print(' '.join(this_cmd))

		retval = subprocess.call(this_cmd)
		results[s] = retval

		# Write this in each loop in case something dies
		f = open(results_path, 'w')
		json.dump(results, f, indent=0, sort_keys=True)
		f.close()

		print(39 * '-')

if __name__ == '__main__':
	main()
