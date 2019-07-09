#!/bin/bash

# check files in all install packages.


checker()
{
local no=0
local all=0
for i in $(rpm -qa)
do

  local nexist=

  for f in $(rpm -ql $i)
  do
    test -f $f || test -d $f || \
    nexist="$f\n${nexist}"
    if [ $(echo $nexist | wc -l) -gt 10 ]; then
      break
      nexist="$nexist\nOmit the rest ..."
    fi
  done
  all=$(expr $all + 1)


  if [ x$nexist != x ]; then
    no=$(expr $no + 1)
    echo $no FAILED: $i missing file\(s\):
    echo -e $nexist
  fi
done

echo Checked $all rpm packages in total, $no failed.

}

checker
