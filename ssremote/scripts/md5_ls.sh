#!/bin/bash
# Get md5sum of sub-directories and files.

file_lister()
{
# list all files(not directory)
  local f_name=$1
  if [ -d $f_name ]; then
#    echo $f_name
    for i in `ls $f_name`
      do
        file_lister $f_name/$i
      done
  else
    md5sum $f_name
  fi
}


file_lister $1
