#!/bin/bash
# A super simple test tool.
# for execute script on remote host.
# By lufei @ 20180801

. ./net_test.sh

# test directory on REMOTE host
test_dir=/opt/ltptest

# result directory on LOCAL host
result_dir=~/results/result

usage()
{
  echo "Usage: $0 -H <HOST> -s <SCRIPT> [-p <PASSWORD>]"
  echo "    Execute SCRIPT on host HOST, and copy results in $test_dir to "
  echo "    local $result_dir."
  echo "    Options:"
  echo "    -p password"
  echo "    -r test direcotry on HOST"
}

main()
{
  if [ x$1 = x ]; then
    usage
    exit 1
  fi
  
  while getopts "H:s:p:r:" arg
    do
      case $arg in
        H) 
           host=$OPTARG ;;
        s) 
           script=$OPTARG ;;
        p)
           password=$OPTARG ;;
        r)
           test_dir=$OPTARG;;
        ?) 
           usage
           exit 1
           ;;
      esac
    done
  
<<!
  if [ x$1 != x ]; then
    echo "Unknown option: $1"
    usage
    exit 1
  fi
!
  
  if [ x"$host" = x -o x"$script" = x ]; then
    echo "HOST and SCRIPT are required." >&2
    usage
    exit 1
  fi
  password=${password:-"abc123"}
  
  if net lookup $host; then
    :
  else
    echo "ERROR: $host cannot be resolved."
    exit 1
  fi
  
  ssh_copy_id $host $password
  if [ -d $result_dir ]; then
    i=0
    while [ -d $result_dir.$i ]
      do
      i=$(($i+1))
      done
    result_dir=$result_dir.$i
  fi
  
  if ssh root@$host [[ -d $test_dir ]]; then
    i=0
    while ssh root@$host [[ -d $test_dir.$i ]]
      do
      i=$(($i+1))
      done
    test_dir=$test_dir.$i
  fi
}


ssh root@$host -- "mkdir -p $test_dir"
scp $script root@$host:$test_dir
scp ./net_test.sh root@$host:$test_dir
scp ./sys_test.sh root@$host:$test_dir
ssh root@$host -- "cd $test_dir; sh $script"

# Copy test results to local.
scp -r root@$host:$test_dir $result_dir
