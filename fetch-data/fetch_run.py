#!/usr/bin/env python
"""A script for fetching files from the Mac Minis.

This script will fetch the specified run from the Mac Minis and
put all of the files in a sensible directory on the local computer.

The fetching is done using an Ansible playbook (through an external
subprocess call), and the rearranging is done with a function in this
file.

After running this command, the files will be found in

    [local_root]/[exp_name]/[run_name]

Usage:

    ./fetch_run.py <exp_name> <run_name> <local_root>

For the experiment name, provide the name of an experiment known to Narval.
For the run name, give a string like 'run_0021' or 'run_0142'.
"""

from __future__ import print_function, division
import os
import sys
import re
import glob
import subprocess
import shutil

def fetch(exp_name, run_name, local_root):
    playbook_path = os.path.expanduser('~/daq-scripts/fetch-data/fetch-file.yml')
    vars_str = 'exp_name={e} run_name={r} local_root={l}'.format(e=exp_name, r=run_name, l=local_root)
    print('Fetching data files:')
    command = ['ansible-playbook', playbook_path, '--extra-vars', vars_str]
    ret = subprocess.call(command)
    if ret != 0:
        raise RuntimeError('Ansible failed to fetch data: code {}'.format(ret))

def rearrange_files(exp_name, run_name, local_root):
    fetch_dir = os.path.join(local_root, exp_name, 'temp')  # where the files are
    clean_dir = os.path.join(local_root, exp_name)
    run_dir = os.path.join(clean_dir, run_name)  # where the files will go

    # Find files for this run

    fileglob = os.path.join(fetch_dir, 'mm?', run_name + '*')
    files = glob.glob(fileglob)

    # Rearrange files

    print('Rearranging files')

    if not os.path.exists(run_dir):
        os.makedirs(run_dir)

    for fp in files:
        # regex matches e.g. '/data/test/temp/mm0/run_0001.dat.10-06-15_11h45m17s'
        # extract the CoBo number from mmN, and keep the timestamp
        regex = r'.*mm(\d)\/' + run_name + r'\.dat\.(.*)'
        m = re.match(regex, fp)

        # rename to CoBoN_run_XXXX_(timestamp).graw
        new_name = "CoBo{}_{}_{}.graw".format(m.group(1), run_name,
                                              m.group(2))
        new_path = os.path.join(run_dir, new_name)

        shutil.move(fp, new_path)

def main():
    if len(sys.argv) < 4:
        sys.exit('Provide experiment name, run name, and local data root')
    exp_name = sys.argv[1]
    run_name = sys.argv[2]
    local_root = sys.argv[3]

    fetch(exp_name, run_name, local_root)
    rearrange_files(exp_name, run_name, local_root)

if __name__ == '__main__':
    main()
