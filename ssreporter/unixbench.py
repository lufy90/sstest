#!/bin/evn python
# coding: utf-8
# unixbench.py

import data
import model
import re

class UnixbenchFile(data.DataFile):
  data_tag = 'Benchmark Run'

  def get_data(self, rown):
    '''get one piece of Unixbench data with given line_id, line_id should \
       be line number of "Benchmark Run"'''
    data = {}

    content = self.get_content()
    for i in reversed(content[0:rown]):
      if 'BYTE UNIX Benchmarks' in i:
        data["Unixbench_Version"] = re.findall('\w\.\w\.\w', i)[0]
        break
      if 'System:' in i:
        data["System"] = i.split(':')[1].lstrip()
      if 'OS:' in i:
        data["OS"] = i.split('--')[1].strip()
      if 'Machine:' in i:
        data["Machine"] = i.split(':')[1].lstrip()

    data["Run time"] = content[rown][15:]
    data["parallel copies"] = int(content[rown + 1].split(' ')[5])
    data["CPUn"] = int(content[rown + 1].split(' ')[0])
    for line in range(rown + 17, rown + 31):
      if content[line].split('  ')[0]:
        line_cont = content[line]
        data[line_cont.split('  ')[0]] = float(line_cont.split(' ')[-1])

    return data

class UnixbenchSheetData(model.WBSheetData):
  header = [['Unixbench Origin Data Page.'],
            ['数据处理：\n１，请将原始数据中的非正常值的背景设置\
为黄色背景;\n２，在计算 "AVG." 时，应过滤掉非正常值\
，并修改取平均数公式中的分母'],
            ]


  data_title_key = 'parallel copies'
  sheet_name = 'OriginData'      # sheet name
  data_class = UnixbenchFile     # UnixbenchFile have get_data() method.
  data_keys = [    # data header by which select data to sheet,
                   # data_keys[0] is specially used to generate 
                   # average line.
             "OS",
             "System Benchmarks Index Score",
             "Dhrystone 2 using register variables",
             "Double-Precision Whetstone",
             "Execl Throughput",
             "File Copy 1024 bufsize 2000 maxblocks",
             "File Copy 256 bufsize 500 maxblocks",
             "File Copy 4096 bufsize 8000 maxblocks",
             "Pipe Throughput",
             "Pipe-based Context Switching",
             "Process Creation",
             "Shell Scripts (1 concurrent)",
             "Shell Scripts (8 concurrent)",
             "System Call Overhead",]


if __name__ == '__main__':
  uf = UnixbenchSheetData()
  uf.data_file_paths = ['samples/test48-2018-12-19-01',
                     'samples/test48-2018-12-19-02',
                     'samples/test48-2018-12-19-03',
                     'samples/deepin-2018-10-28-01',
                     'samples/deepin-2018-10-28-02',
                     'samples/deepin-2018-10-28-03',
                     ]

#  print(uf.get_all_data())
  uf.save_to_sheet()
  uf.wb.save('UnixbenchTestReport.xls')

