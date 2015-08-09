#!/usr/bin/env python3
"""split_config.py

Use this script to take a config file with nodes for each CoBo into a set of
config files with one CoBo per file.

"""

import xml.etree.ElementTree as et
import copy
import os
import sys

def split(filename):

    config_name = os.path.splitext(os.path.basename(filename))[0]
    config_path = os.path.dirname(filename)

    print('Reading', filename)
    with open(filename) as f:
        tree = et.parse(f)

    for x in range(10):
        tree_copy = copy.deepcopy(tree)
        root = tree_copy.getroot()
        cobo = root.find('./Node[@id="CoBo"]')
        for inst in cobo.findall('./Instance'):
            if inst.get('id') not in [str(x), '*']:
                cobo.remove(inst)
        cobo.find('./Instance[@id="{}"]'.format(x)).set('id', '0')

        outfile = os.path.join(config_path, config_name + '_' + str(x) + '.xcfg')
        print('Writing', outfile)
        tree_copy.write(outfile)

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        sys.exit('Provide a config path as the first argument')

    split(filename)
