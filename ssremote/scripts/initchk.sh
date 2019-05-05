#!/bin/bash
# initchk.sh
# for init check about a OS installation.


# check /var/log/

grep -r -i fail /var/log/ > log_fail.stdout
grep -r -i error /var/log/ > log_error.stdout

