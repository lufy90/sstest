#!/bin/env python36
# test.py
# a demo and basic type of test.


'''Basic types of all tests. '''

import time
from remote import ssh
from scp import SCPClient
import time
import os
from setting import RESULT_DIR as rs

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
  r_results = ''
  interval = 10
  def __init__(self, module_name):
    self.tst_time = time.strftime('%Y%m%d %H%M%S', time.localtime())
    self.name = type(self).__name__
    self._module_name = module_name
    self.l_results = rs + '/' + module_name + '/' + self.name + self.tst_time.split()[0]
    self.l_results = "%s/%s/%s/%s" % (rs, module_name, self.name, 'rs' + self.tst_time.split()[0])
    os.makedirs(self.l_results, exist_ok=True)

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
    else:
      if self.script:
        pass
    print('####################### TEST INFO #########################')
    print('# name: %-49s #' % self.name)
    print('# doc: %-50s #' % self.__doc__)
    print('# start: %-48s #' % self.tst_time)
    print('# user: %-49s #' % self.user)
    print('# host: %-49s #' % self.host)
    print('# script: %-47s #' % self.script)
    print('# iteration: %-44s #' % self.iteration)
    print('###########################################################')
    print('')
  def exe_test(self, iter_num):
    '''execute test '''
    # self.ex_rhost(self.host, self.cmd, self.tst_user, self.tst_password)
    if self.host:
      ssh_client = ssh(self.user, self.host, self.password)
      stdin, stdout, stderr = ssh_client.exec_command(self.cmd, get_pty=True, timeout=self.timeout)
      with open(self.l_results + '/stdout.' + str(iter_num), 'wb') as f:
        while True:
          c = stdout.read(1024)
          if not c:
            break
          f.write(c)
      with open(self.l_results + '/stderr.' + str(iter_num), 'wb') as f:
        while True:
          c = stderr.read(1024)
          if not c:
            break
          f.write(c)
    else:
      pass

  def suf_test(self):
    '''results collection and cleaning '''
    if self.host and self.script:
      if self.r_results:
        ssh_client = ssh(self.user, self.host, self.password)
        scp_client = SCPClient(ssh_client.get_transport())
        scp_client.get(self.r_results, self.l_results, recursive=True)
        ssh_client.close()
        scp_client.close()

  def run(self):
    '''run test'''
    self.pre_test()
    for i in range(self.iteration):
      print('#%d' % i)
      self.exe_test(i)
      if i < self.iteration -1 :
        time.sleep(self.interval)
    self.suf_test()

  def banner(self):
    pass
