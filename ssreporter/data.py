#!/bin/env python
# 20181220

import re

class DataFile(object) :
  data_tag = ''   # uniq mark of a data piece.
  def __init__(self, path):
    self.path = path
    self.name = path.split('/')[-1]
  def get_content(self):
    with open(self.path, 'r') as f:
       content = [ x.replace('\n','') for x in f.readlines()]
    return content

  def get_tag_rowns(self):
    ''' row numbers of data_tag'''
    rowns = []
    content = self.get_content()
    for i in range(len(content)):
      if self.data_tag in content[i]:
        rowns.append(i)
    return rowns

  def get_data(self, rown):
    ''' get data from files '''
    return ''

  def get_all_data(self):
    ''' returns all data as list contained data dictionaries '''
    data_rowns = self.get_tag_rowns()
    d=[]
    for i in data_rowns:
      d.append(self.get_data(i))
    return ListOfDictionaries(d)

  
class ListOfDictionaries(list):
  ''' list of dictionaries, data from one or multipul files. '''

  def get_values_by_key(self, key):
    ''' key: data index, return list of data non repeatedly '''
    k = []
    for d in self:
      k.append(d[key])
    ks = list(set(k))
    ks.sort(key=k.index)
    return ks

  def get_data_by_kv(self, kv):
    ''' kv: {key: value}, return a ListOfDictionaries instance that [key] == value '''
    d = []
    for i in self:
      for key in kv.keys():
        ok = False
        if i[key] == kv[key]:
          ok = True
      if ok:
        d.append(i)
    return ListOfDictionaries(d)

  def get_data_size(self):
    coln = 0
    for i in self:
      if coln < len(i):
        coln = len(i)
    return(len(self), coln)

  def get_values_by_keys(self, keys):
    ''' keys: a list of data indexes, return a list include a data list specified by keys  '''
    values = []
    for i in self:
      kvalues = []
      for j in keys:
        kvalues.append(i[j])
      values.append(kvalues)
    return values

