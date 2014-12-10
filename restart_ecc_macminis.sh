#!/bin/bash

echo "Restarting all ECC servers\n"

sudo ansible macminis -m shell -a "systemctl restart ecc"
