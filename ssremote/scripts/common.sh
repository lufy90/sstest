#!/bin/bash

ss_dirname(){
  local dirname=$1
  if [ -d $dirname ]; then
    local i=1
    while [ -d $dirname.$i ]; do
      i=$((i+1))
      done
  fi
  echo $dirname.$i
}

