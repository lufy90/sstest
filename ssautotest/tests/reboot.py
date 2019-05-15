#!/bin/env python36
#
# reboot test.

'''for reboot test -- this test can NOT run at LOCAL host'''

from . import test


class reboot(test.Test):
  iteration = 1

class reboot1(test.Test):
  pass
