#!/bin/env python36
# test.py
# a demo and basic type of test.


'''Basic types of all tests. '''

import time
from remote import ssh
from scp import SCPClient
import time




class Test():
  '''test demo, all other tests are subclasses of this one. '''
  user = 'root'
  password = 'abc123'
  script = ''              # if defined, then scp script to host
  iteration = 3
  host = ''
  cmd = ''
  timeout = 10
  tst_dir = '/tmp/'
  results = ''
  interval = 10
  ldir = '/tmp/'
  def __init__(self):
    self.tst_time = time.strftime('%Y%m%d %H%M%S', time.localtime())
    self.name = type(self).__name__

  def pre_test(self):
    '''Settings before test '''
    if self.host:
      # test on specified host.
      if self.script:
        # cp or scp script to test directory.
        ssh_client = ssh(self.user, self.host, self.password)
        scp_client = SCPClient(ssh_client.get_transport())
        scp_client.put(self.script, self.tst_dir, recursive=True)
        ssh_client.close()
        scp_client.close()
    print('####################### TEST INFO #########################')
    print('# name: %-49s #' % self.name)
    print('# start: %-48s #' % self.tst_time)
    print('# user: %-49s #' % self.user)
    print('# host: %-49s #' % self.host)
    print('# script: %-47s #' % self.script)
    print('# iteration: %-44s #' % self.iteration)
    print('###########################################################')
    print('')
  def exe_test(self):
    '''execute test '''
    # self.ex_rhost(self.host, self.cmd, self.tst_user, self.tst_password)
    if self.host:
      ssh_client = ssh(self.user, self.host, self.password)
      stdin, stdout, stderr = ssh_client.exec_command(self.cmd, get_pty=True, timeout=self.timeout)
      while True:
        c = stdout.read(1024)
        if not c:
          break
        print('STDOUT:',c)
      while True:
        c = stderr.read(1024)
        if not c:
          break
        print('STDERR', stderr.read(1024))
    else:
      pass

  def suf_test(self):
    '''results collection and cleaning '''
    if self.host and self.script:
      if self.results:
        ssh_client = ssh(self.user, self.host, self.password)
        scp_client = SCPClient(ssh_client.get_transport())
        scp_client.get(self.results, self.ldir, recursive=True)
        ssh_client.close()
        scp_client.close()

  def run(self):
    '''run test'''
    self.pre_test()
    for i in range(self.iteration):
      self.exe_test()
      if i < self.iteration -1 :
        time.sleep(self.interval)
    self.suf_test()

  def banner(self):
    pass
