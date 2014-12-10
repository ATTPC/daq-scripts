#!/bin/bash

echo "Killing Narval processes on Mac Minis\n"

sudo ansible macminis -m shell -a "pkill gnarval"
