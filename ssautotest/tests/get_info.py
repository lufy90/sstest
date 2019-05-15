#!/bin/env python36

from . import test
from .hosts import test_183

class info(test.Test):
  host='192.168.45.183'
  script='./scripts/info.sh'
  cmd='cd %s;./info.sh' % test.Test.tst_dir
