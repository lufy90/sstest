#!/bin/env python
# remote.py
# 20190220

# requires: sshpass

import os, sys, getopt

class Script():

  def __init__(self, file_name):
    self.file_name = file_name
    self.name = file_name.split('/')[-1]

def main(argv):
  help_info = "Usage: %s -H host -s script [-u user] [-p password]\
 [-r testdirectory]" % argv[0]
  try:
    opts, args = getopt.getopt(argv[1:], 'hH:s:u:p:r:o:')
  except getopt.GetoptError:
    print(help_info)
    sys.exit(2)

# Default paramaters
  host = ''
  script = ''
  tst_dir = '/tmp/sstest'
  user = 'root'
  password = 'abc123'


  for opt, arg in opts:
    if   opt == '-h':
      print(help_info)
      sys.exit(2)
    elif opt == '-H':
      host = arg
    elif opt == '-s':
      script = arg
    elif opt == '-u':
      user = arg
    elif opt == '-p':
      password = arg
    elif opt == '-r':
      tst_dir = arg
    elif opt == '-o':
      rslt_dir = arg

  if not (host and script):
    print(help_info)
    sys.exit(2)

  def exe_on_remote(host, command, user=user, password=password):
    host = user + '@' + host
    prefix = 'sshpass -p %s ssh -o StrictHostKeyChecking=no %s ' % (
            password, host)
    return os.system(prefix + command)

  script = Script(script)
#  ssh_options = '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/tmp/known_hosts'
  if exe_on_remote(host, '[ -d %s ]' % tst_dir) == 0:
    ''' if tst_dir already exists on host '''
    i = 0
    while exe_on_remote(host, '[ -d %s ]' % (tst_dir + str(i).zfill(2))) == 0:
      i += 1
    tst_dir = tst_dir + str(i).zfill(2)

  if exe_on_remote(host, 'mkdir -p %s' % tst_dir) != 0:
    print("Error: mkdir %s failed." % tst_dir)

  os.system('sshpass -p %s scp -o StrictHostKeyChecking=no %s %s@%s' % (
             password, script.file_name, user, host+':/'+tst_dir))
  exe_on_remote(host, '\'cd %s; bash ./%s\'' % (tst_dir, script.name))


if __name__ == '__main__':
  main(sys.argv)
