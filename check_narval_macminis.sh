#!/bin/bash

echo "Checking for running Narval processes on Mac Minis\n"

ansible macminis -m shell -a "ps -e | grep gnarval"
