#!/bin/env python36


from . import test
class ls(test.Test):
  script = './scripts'
  user = 'lufei'
  host = '10.1.1.14'
  cmd = 'ls'
  iteration = 2
