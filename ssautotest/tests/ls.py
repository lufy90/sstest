#!/bin/env python36


from . import test
class ls(test.Test):
  script = './scripts'
  user = 'lufei'
  host = 'localhost'
  cmd = 'ls'
