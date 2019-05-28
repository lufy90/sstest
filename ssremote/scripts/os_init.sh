#!/bin/bash
# os_init.sh
# get initial status of installed os

ini_dir=${HOSTNAME}-init
mkdir $init_dir


uname -a > init_dir/uname_-a
uptime > $init_dir/uptime
cp /var/log -r $init_dir/
rpm -qa > $init_dir/rpm_-qa


