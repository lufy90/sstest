#!/bin/bash
# A super simple test tool.
# for execute script on remote host.
# By lufei @ 20180801

#. ./net_test.sh

# test directory on REMOTE host

test_dir=/opt/tests
result_dir=~/results/result
tst_user=root
tst_pass=abc123

echo "Differ from remote.py, copies result back, remote.py not"
usage()
{
  echo "Usage: $0 -H host -s script [-p password] [-r testdirectory]"
}

#exe_on_remote()
#{
#  local password=$1
#  local host=$2
#  local cmd=$3
#  sshpass -p $password ssh -o StrictHostKeyChecking=no $host '$cmd'
#}

main()
{
#  if [ x$1 == 'x' ]; then
#    usage
#    exit 1
#  fi
  
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
  
  if [ x"$host" = x -o x"$script" = x ]; then
#    echo "HOST and SCRIPT are required." >&2
    usage
    exit 1
  fi
  password=${password:-"abc123"}
  
#  ssh_copy_id $host $password
  if [ -d $result_dir ]; then
    i=0
    while [ -d $result_dir.$i ]
      do
      i=$(($i+1))
      done
    result_dir=$result_dir.$i
  else mkdir -p $result_dir
  fi
  
  if sshpass -p $password ssh root@$host [[ -d $test_dir ]]; then
    i=0
    while sshpass -p $password ssh root@$host [[ -d $test_dir.$i ]]
      do
      i=$(($i+1))
      done
    test_dir=$test_dir.$i
  fi
}


main $@
sshpass -p $password ssh root@$host -- "mkdir -p $test_dir"
sshpass -p $password scp $script root@$host:$test_dir
sshpass -p $password ssh root@$host -- "cd $test_dir; sh ${script##*/}"

# Copy test results to local.
sshpass -p $password scp -r root@$host:$test_dir $result_dir
