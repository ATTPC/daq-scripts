#!/usr/bin/env python3
from __future__ import print_function, division
import glob
import os
import sys
import re
import shutil
from socket import gethostname


def backup_configs(run_num):
    # Find the output path
    configs_path = '/daq/Configs'
    output_path = '/data/e15503-data/configs'
    config_files = glob.glob(os.path.join(configs_path, '*.xcfg'))
    print('Found %d config files' % len(config_files))

    new_folder_name = 'run_{:04d}'.format(run_num)

    # Make the run folder as "run_0000", for example
    full_newdir = os.path.join(output_path, new_folder_name)
    os.makedirs(full_newdir)

    # Copy the config files to the run folder
    print('Copying xcfg files')
    for cf in config_files:
        shutil.copy(cf, full_newdir)


if __name__ == '__main__':
    try:
        run_num = int(sys.argv[1])
    except IndexError:
        sys.exit('Provide run number as first argument')
    except TypeError:
        sys.exit('Run number must be an integer')

    backup_configs(run_num)
