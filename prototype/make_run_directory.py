#!/usr/bin/env python
from __future__ import print_function, division
import glob
import os
import sys
import re
import shutil

# import tkinter as tk

def rearrange_files():
    # Find the output path
    datapath = '/Volumes/July2015Data'
    config_files = glob.glob(os.path.join(datapath, '*.xcfg'))
    print('Found %d config files' % len(config_files))

    # Find existing run folders
    run_folders = glob.glob(os.path.join(datapath, 'run*'))
    print('%d run folders exist' % len(run_folders))

    # Find the existing run numbers, and set the new one to be the next integer
    run_nums = [int(re.match(r'.*run_(\d{4})$', r).groups(1)[0]) for r in run_folders]
    if len(run_nums) > 0:
        next_run_num = max(run_nums) + 1
    else:
        next_run_num = 0

    new_folder_name = 'run_{:04d}'.format(next_run_num)
    print('This run will be called %s' % new_folder_name)

    # Make the run folder as "run_0000", for example
    full_newdir = os.path.join(datapath, new_folder_name)
    assert full_newdir not in run_folders, 'ERROR: Run folder already exists'
    os.makedirs(os.path.join(datapath, new_folder_name))

    # Copy the config files to the run folder
    print('Copying xcfg files')
    for cf in config_files:
        shutil.copy(cf, full_newdir)

    # Now find the data files and copy them
    datafiles = glob.glob(os.path.join(datapath, '*.graw'))
    if len(datafiles) == 0:
        print('There were no datafiles in the data directory.')
        sys.exit(0)
    else:
        print('Found %d data files' % len(datafiles))

    # Parse the datafile names to make sure the timestamps match
    graw_regex = r'CoBo_AsAd0_(?P<timestamp>.*)_(?P<index>\d{4}).graw'
    matches = [re.search(graw_regex, p) for p in datafiles]
    timestamps = []
    indices = []
    for m in matches:
        assert m is not None, 'Regex match on filename failed'
        gd = m.groupdict()
        timestamps.append(gd.get('timestamp'))
        indices.append(gd.get('index'))

    if len(set(timestamps)) > 1:
        # This checks if the timestamps are all identical
        print('More than one run exists in the output directory.')
        print('I can\'t copy the files automatically, so do it manually. Sorry!')
        sys.exit(1)

    if len(set(indices)) != len(indices):
        # This checks that the indices are unique
        print('Two runs had the same index... failing.')
        sys.exit(2)

    # Actually move the files now
    print('Moving data files')
    for df in datafiles:
        shutil.move(df, full_newdir)

    print('Finished')
    print('Files are now in %s' % full_newdir)
    print('Datafile names:')
    for df in datafiles:
        print('    %s' % df)

if __name__ == '__main__':
    rearrange_files()

# class Application(tk.Frame):
#     def __init__(self, master=None):
#         tk.Frame.__init__(self, master)
#         self.pack()
#         self.createWidgets()
#
#     def createWidgets(self):
#         self.rearrange_button = tk.Button(self, text='Rearrange', height=2,
#                                                 command=lambda: print('text'),
#                                                 padx=20)
#         self.rearrange_button.pack(side='top', fill=tk.X)
#
#         self.exit_button = tk.Button(self, text='Quit', command=root.destroy,
#                                      height=2, padx=20)
#         self.exit_button.pack(side='bottom', fill=tk.X)
#
# if __name__ == '__main__':
#     root = tk.Tk()
#     root.title('Rearranger')
#     app = Application(master=root)
#     app.mainloop()
