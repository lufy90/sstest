#!/bin/env python

'''
  getting cammands output to files.
  by lufei
  version: 1.0
  Known bugs:
    a. NOT support wildcard.
    b. Can NOT read file with same file name under different directory.
'''

import os, sys, commands, socket

# Add commands in cmd list.
cmd = [
  "ifconfig",
  "rpm -qa",
  "cat /proc/cpuinfo",
  "cat /proc/cpuinfo",
  "lspci -vvv",
  "dmidecode",
  "free -m",
  "date",
  "lscpu",
  # disk info
  "lsblk",
  "fdisk -l",
  "lshw",
  ]

cmd = list(set(cmd)
)
PREFIX="./hwc-"
dir_name = PREFIX + socket.gethostname()

if os.path.exists(dir_name):
  i = 0
  while os.path.exists(dir_name+'.'+str(i)):
    i = i + 1
  dir_name = dir_name+'.'+str(i)

os.mkdir(dir_name)

for itm in cmd:
  itm_file = dir_name + "/" + itm.replace(" ", "_").split('/')[-1]
  (stat, output) = commands.getstatusoutput(itm)

  if stat != 0:
    print('FAILED CMD: ' + output)
  else:
    print('EXECUTING: ' + itm + '...')
    with open(itm_file, 'w') as f:
      f.write(output)
