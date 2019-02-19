#!/bin/env python
# coding=utf-8
# model.py
# 20181224


import data
import xlrd, xlwt, xlutils

#### Settings #####
test_oses = [
  {
   "name": "CentOS", 
   "data_file": ['samples/unixbench_isoft/test48-2018-12-19-01',
                 'samples/unixbench_isoft/test48-2018-12-19-02',], },

  {
   "name": "Ubuntu", 
   "data_file": ['samples/unixbench_isoft/test48-2018-12-19-03',], },
]

###################
class WorkSheet():
  '''  workbook = xlwt.Workbook()
  def __init__(self, name, *k, **kw):
    super(WorkSheet, self).__init__(name, self.workbook, *k, **kw)
  '''
  def __init__(self, sheet):
    self.sheet = sheet
  def write_data(self, data):
    self.sheet.write(0,0, data)

class WBSheetData():
  data_file_paths = []
  header = [[],[],]
# ----------------------------------------
  data_title_key = ''
  data_keys = []
  data_class = data.DataFile
  sheet_name = ''   # sheet name
  wb = xlwt.Workbook(encoding='utf-8')
  def __init__(self):
    self.sht = self.wb.add_sheet(self.sheet_name)

  def get_data_files(self):
    return [ self.data_class(x) for x in self.data_file_paths ]

  def get_all_data(self):
    ''' get data from multiple DataFiles '''
    d = data.ListOfDictionaries()
    for i in self.get_data_files():
      d += i.get_all_data() 
    return d

  def save_to_sheet(self):
    all_data = self.get_all_data()
    title_data = all_data.get_values_by_key(self.data_title_key)
    ir, ic = 0,0
    ir, ic = self.write_to_block(self.sht, self.header, first_cell = (ir, 0))
    for i in title_data:
      ir = self.write_to_row(self.sht, ['%s:%s' % 
                                  (self.data_title_key, str(i))], rown = ir)
      d = all_data.get_data_by_kv({self.data_title_key:i})
      d_title_data = d.get_values_by_key(self.data_keys[0])
      ir, ic = self.write_to_block(self.sht, [self.data_keys], 
                                   first_cell=(ir, 0))
      for j in d_title_data:
        d1 = d.get_data_by_kv({self.data_keys[0]:j})
        d1_values = d1.get_values_by_keys(self.data_keys)
        ir, ic = self.write_to_block(self.sht, d1_values, first_cell = (ir ,0))
        average_title = 'AVG' 
        self.sht.write(ir, 0, average_title)
        for col in range(1,len(self.data_keys)):
          col_26 = decimal_to_x(col, 26)
          average_definition = '%s:%s' % (col_26+str(ir-len(d1)+1), 
                                          col_26+str(ir))
          self.sht.write(ir, col,
                         xlwt.Formula('AVERAGE(%s)'%average_definition))
        ir += 1
      ir += 1

  def write_to_block(self, sht, data, first_cell=(0,0)):
    ''' data: [[1,2,3],[4,5,6]]'''
    ir = first_cell[0]
    for i in data:
      ic = first_cell[1]
      for j in i:
        sht.write(ir, ic, j)
        ic += 1
      ir += 1
    return (ir, ic)

  def write_to_row(self, sht, data, rown=0):
    ''' data: [1,2,3,]  '''
    coln = 0
    for i in data:
      sht.write(rown, coln, i)
      coln += 1
    return rown+1

def decimal_to_x(n, x, u='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
  quo = n // x
  rem = n % x
  res = []
  res.append(u[rem])

  while True:
    if not quo:      
      break
    rem = quo % x
    quo = quo // x
    res.append(u[rem])

  res.reverse()
  return ''.join(res)

def save_to_excel(excel_name, excel_data):
  ''' eg. excel_data = [{"name":sheet_name1, 
                         "data":[[a00,a01,a02],[a10,a11,a12]]},
                        {"name":sheet_name2,
                         "data":[[b00,b01,b02],[b10,b11,b12]]},]
  '''
  wb = xlwt.Workbook(encoding='utf-8')
  for sht_data in excel_data:
    sht=wb.add_sheet(sht_data['name'])
    for nrow in range(len(sht_data['data'])):
      for ncol in range(len(sht_data['data'][nrow])):
        sht.write(nrow, ncol, sht_data['data'][nrow][ncol])
  wb.save(excel_name)



