#!/bin/env python36
# remote.py
# execute executable on remote host.
# lufy @ 20190505


import paramiko
import sys
import os
import pkgutil
import lib
import importlib

###########
import warnings
warnings.filterwarnings(action='ignore', module='.*paramiko.*')



class Main():
  def __init__(self):
    self.name = sys.argv[0]
    self.args = sys.argv[2:]
    try:
      self.opt = sys.argv[1]
    except IndexError as e:
      self.opt = 'help'

  def execute(self, options):
    ''' options: class of options '''
    opts = options(self.opt, self.args)
    opts.execute()

class Options():
  def __init__(self, name, args=None):
    self.name = name
    self.args = args
    self.call_options = {
      'help': self.usage,
      'list': self.listall,
      'run': self.run,
      'create': self.create,
      } 

  def usage(self, *args, **kwargs):
    '''print this help. '''
    print('Usage:')
    for i in self.call_options.keys():
      print(' %-6s %s' % (i, self.call_options[i].__doc__))

  def listall(self, args=None):
    '''list available test modules -- [all|<testmodul>] list all|test in <testmodule>'''
    default_name = 'tests'  ############### NEED TO IMPROVE

    if args:
      if args[0] == 'all':
        tst_modules = []
        lib.get_sub(default_name, tst_modules)
        for i in tst_modules:
          print('\033[1;34m %-20s\033[0m%s' % (i.__name__, i.__doc__))
          for t in lib.get_tests(i):
            print('  %-19s%s' % (t.__name__, t.__doc__))
      else:
        for m_name in args:
          try:
            tst_module = importlib.import_module(m_name)
            print('In module \033[1;34m %s\033[0m:' % m_name)
            for t in lib.get_tests(tst_module):
              print('  %-10s%s' % (t.__name__, t.__doc__))
          except Exception as e:
            print('failed to import such module: %s' % m_name)
            print(e)
#            sys.exit(2)
        
    else:
      tst_modules = []
      lib.get_sub(default_name, tst_modules)
      for i in tst_modules:
        print('\033[1;34m %-20s\033[0m%s' % (i.__name__, i.__doc__))
 
#    tst_modules = []
#    lib.get_sub(default_name, tst_modules)
#    for i in tst_modules:
#      print('\033[1;34m %-20s\033[0m%s' % (i.__name__, i.__doc__))
#      # if arguments given, invoke lib.get_tests.
#      
#      if args and args[0] == '-v':
#        for t in lib.get_tests(i):
#          print('  %-19s%s' % (t.__name__, t.__doc__))
      

  def run(self, args):
    '''run test -- <test_module>  [<test_name1> [<test_name2>]] run test(s) in test_module. If no test_name specified, run all tests in test_module'''
    try:
      m_name = args[0]
      t_names = args[1:]
    except Exception as e:
      print('%s\n%s'%(e,self.run.__doc__))
      sys.exit(1)

    if t_names:
      for t_name in t_names:
        t = lib.get_test_m(m_name, t_name)
        if not t:
          print('test not found: %s in %s'%(t_mame, m_name))
          sys.exit(2)
        t_instanse = t()
        t_instanse.run()
    else:
      try:
        m = importlib.import_module(m_name)
      except Exception as e:
        print(e)
        print('failed import test module: %s' % m_name)
        sys.exit(2)
      for t in lib.get_tests(m):
        t_instanse = t()
        t_instanse.run()

  def runall(self, args):
    '''runall tests in given module -- merged in to option run.'''  # Maybe could be merged in run function.
                                        # if merged, cannot run multipul module
                                        # at a same time in command line args.
    pass

  def execute(self):
    try:
      self.call_options[self.name](self.args)
    except KeyError as e:
      print('Unknown option: ',self.name)
      self.call_options['help'](self.args)

  def create(self, args):
    '''create test template -- <testname>'''
    if not args:
      print(self.create.__doc__)
      sys.exit(1)
#    for tem in args:
#      with open('./tests/%s', 'wb') as f:
#        f.write(template_content)

if __name__ == '__main__':
  main = Main()
  main.execute(Options)
