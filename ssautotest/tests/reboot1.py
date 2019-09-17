#!/bin/env python36
#
# reboot test.

'''for reboot test -- this test can NOT run on localhost'''

from . import test


class reboot(test.Test):
  iteration = 1
  interval = 500
  cmd = 'reboot'

class reboot1(test.Test):
  pass
