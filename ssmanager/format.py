#!/bin/env python
# format.py
# Classes about 
# 20181126

import xlwt
import xlrd
from xlutils.copy import copy
import database

#################################################
# Settings
Db = database.Sqlite3

#################################################

class Excel(object):
  def __init__(self, path):
    self.path = path
    self.name = path.split('/')[-1]
    try:
      self.wb = xlrd.open_workbook(self.path)
      # try if file not exists, then create.
    except IOError,e:
      init_sheet="sheet0"
      print("%s\nNow create new excel file with %s: %s" % 
             (e, self.path, init_sheet)
           )
      self.wb = xlwt.Workbook()
      self.wb.add_sheet(init_sheet)
      self.wb.save(self.path)
      self.wb = xlrd.open_workbook(self.path)

    self.nsht = self.wb.nsheets

  def show_summary(self):
    output = "File \33[1m%s\33[0m includes %d sheet(s) in total:"
    print(output % (self.name, self.wb.nsheets))
    sheet_disc = "  Sheet%d: %s\n\
  Include: %d line(s) and %d column(s)\n\
  First cell: %s\n"
    for sht in self.wb.sheets():
      if sht.nrows and sht.ncols:
        cell_0 = sht.cell(0,0).value
      else:
        cell_0 = None
      sheet_summ = (sht.number, sht.name, sht.nrows,
                    sht.ncols, cell_0)
      print(sheet_disc % sheet_summ)

  def convert_to_json(self, json_file):
    pass

  def add_sht(self,sht_name):
    if sht_name in self.wb.sheet_names():
      print("Sheet name duplicated: %s" % sht_name)
      exit()
    wb = copy(self.wb)
    sht = wb.add_sheet(sht_name)
    wb.save(self.path)

  def save_to_db(self, *a, **k):
    for index in range(self.wb.nsheets):
      sht = Sheet(self.path, index)
      sht.save_to_db(*a, **k)

class Sheet(object):
  def __init__(self, file_path, index):
    self.excel = Excel(file_path)
    self.wb = self.excel.wb
    self.index = index
    self.sht = self.wb.sheet_by_index(index)
    self.cell = self.sht.cell
    self.name = self.sht.name
    
  def show_summary(self, row=5, col=5, sep='\t'):
    if row > self.sht.nrows:
       row = self.sht.nrows
    if col > self.sht.ncols:
       col = self.sht.ncols
    title = "Sheet name: \33[1m%s\33[0m\nIndex: %s\n%dx%d Contents:"
    header = "c/r"

    print(title % (self.name, self.index, row, col))
    for i in range(col):
      header = header + sep + str(i) 
    print(header)
    
    for i in range(row):
      content = str(i) 
      for j in range(col):
        content = content + sep + str(self.sht.cell_value(i,j))
      print(content)

  def save_to_db(self, db_name=None, tb_name=None, 
                 begin=None, end=None, 
                 ):
    if db_name is None:
      db_name = self.excel.name + '.db'
    if tb_name is None:
      tb_name = self.name
    if begin is None:
      begin=(0,0)
    if end is None:
      end=(self.sht.nrows, self.sht.ncols)
                 
    db = Db(db_name)
    dt = ['c'+str(i) for i in range(begin[1], end[1])]
    dt.insert(0, 'id')
    tb_definition = ','.join(dt)
    db.create_tb(tb_name, tb_definition)
    for row in range(begin[0], end[0]):
      dt = ['%s' % row]
      for col in range(begin[1], end[1]):
        dt.append("'%s'" % self.sht.cell(row, col).value)
      dt_definition = ','.join(dt)
      db.insert_dt(tb_name, dt_definition)

class Sql_definition(object):
  ''' convert data to database schema '''
  def __init__(self, describe):
    self.describe = describe

if __name__ == '__main__':
  pass
