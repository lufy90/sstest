#!/bin/env python36
# lib.py
# 


import pkgutil
import sys
import importlib
from tests.test import Test



class Colors:
  ''' Colors class:reset all colors with colors.reset; two  
  sub classes fg for foreground  
  and bg for background; use as colors.subclass.colorname. 
  i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,  
  underline, reverse, strike through, 
  and invisible work with the main class i.e. colors.bold '''

  reset='\033[0m'
  bold='\033[01m'
  disable='\033[02m'
  underline='\033[04m'
  reverse='\033[07m'
  strikethrough='\033[09m'
  invisible='\033[08m'
  class fg: 
    black='\033[30m'
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    lightgreen='\033[92m'
    yellow='\033[93m'
    lightblue='\033[94m'
    pink='\033[95m'
    lightcyan='\033[96m'
  class bg: 
    black='\033[40m'
    red='\033[41m'
    green='\033[42m'
    orange='\033[43m'
    blue='\033[44m'
    purple='\033[45m'
    cyan='\033[46m'
    lightgrey='\033[47m'

  def print_format_table(self): 
    """ 
    prints table of formatted text format options 
    """
    for style in range(8): 
      for fg in range(30, 38): 
        s1 = '' 
        for bg in range(40, 48): 
          format = ';'.join([str(style), str(fg), str(bg)]) 
          s1 += '\x1b[%sm %s \x1b[0m' % (format, format) 
        print(s1) 
      print('\n')

def get_sub(pkg_name, sub_modules):
  ''' get a list of all modules in pkg_name, sub_modules should be a empty list. '''
  try:
    pkg = importlib.import_module(pkg_name)
    for _, sub_name, ispkg in pkgutil.iter_modules(pkg.__path__):
      if ispkg:
        get_sub(pkg.__name__+'.'+sub_name, sub_modules)
      else:
        sub_modules.append(importlib.import_module(pkg.__name__+'.'+sub_name))

  except Exception as e:
    print(type(e).__name__, e)

def get_tests(module):
  '''get all test classes from module even those in sub modules'''
  try:
    if hasattr(module, '__path__'):
      # module is a package
      sub_modules = []
      get_sub(module.__name__, sub_modules)   # get sub only accept strings.
      tst = []
      for mod in sub_modules:
        tst = tst + get_tests(mod)
      return tst
    else:
      return [x for x in vars(module).values() if issubclass_i(x,Test)]   ## NEED TO PROVING
  except Exception as e:
    print(e)
    return []

def issubclass_i(a,b):
  try:
    return issubclass(a,b)
  except TypeError:
    return False

def get_tests_m(m_name, t_names):  # not used by now
  '''get all test classes in m_name module'''
  tests = []
  for t_name in t_names:
    try:
      tests.append(getattr(importlib.import_module(m_name), t_name))
    except Exception as e:
      print(e)
  return tests

def get_test_m(m_name, t_name):
  '''get test class by t_name inside test module m_name'''
  try:
    return getattr(importlib.import_module(m_name), t_name)
  except Exception as e:
    print(e)
    return None
