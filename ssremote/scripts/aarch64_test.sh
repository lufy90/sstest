#!/bin/bash
# filename: aarch64_test.sh
# Author: lufei
# Date: 20200311 16:48:50



directory=info
mkdir $directory
rpm -qa > $directory/rpm_-qa
dmesg >  $directory/dmesg
cp /root/anaconda-ks.cfg $directory/
cp /var/log/messages $directory/

