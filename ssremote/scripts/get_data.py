#!/bin/env python


# for sw64 OS test vmstat output .
def get_lines(i,l,d,fname, oname):
  ''' i: start line
      l: end line
      d: step '''
#  b = open(oname, 'w')
  with open(fname, 'r') as f:
    c = i
    content = "65  0      0 42891680  77800 308608    0    0    22    64  253   37 12  3 85  0  0".split()
    for line in f.readlines():
      if '---' in line or 'swpd' in line:
        continue
      c = c + 1
      if c > l :
        break
      if (c-i)%d == 0:
#        b.write(line)
        avg = get_avg(content, line.split())
        content = avg
  return avg
#        for cc in content:

#  b.close()

def get_avg(a, b):
  ''' a = [2 ,], b = [3,] '''
  a = [ int(x) for x in a]
  b = [ int(x) for x in b]
  c = []
  for i in range(len(a)):
    c.append((a[i]+b[i])/2)
  return c

if __name__ == '__main__':
  import sys
  print get_lines(0, 10, 1, sys.argv[1], sys.argv[2])

