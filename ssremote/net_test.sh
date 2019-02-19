#!/bin/bash
# common used functions.
# 20180621, by lufei



ssh_copy_id()
{
  local user=${user:-"root"}
  local ssh_port=${ssh_port:-22}
  local host=${1:-$host}
  local password=${2:-"abc123"}


  if which expect > /dev/null 2>&1; then
    :
  else
    echo "FAIL: expect not found."
    exit 1
  fi
  echo "Try if ssh key was already copied ..."
  local test_user=`timeout -k 5 30 ssh $user@$host -- whoami`
  if [[ $test_user = $user ]];then
    echo "ssh id already exists."
  else

    if [ ! -f "$HOME/.ssh/id_rsa" ];then
      expect -c "
      spawn ssh-keygen
      expect \"Enter file*\"
      send \"\r\"
      expect \"Enter passphrase*\"
      send \"\r\"
      expect \"Enter same *\"
      send \"\r\"
      expect eof
      "
    fi
  
    expect -c "
      set timeout 30
      spawn ssh-copy-id $user@$host
      expect {
        *yes/no* { send -- \"yes\r\"; exp_continue; }
        *assword: { 
            send -- \"$password\r\"
            expect \"Now try logging into the machine*\" {
            send_user \"Copy ssh id succeeded.\n\"; exp_continue  }
            expect  \"\[Pp\]ermission denied*\" {
            send_user \"\nFAILED copy, permission denied.\n\"; exit 1 }
         }
      }
      expect eof
    " 
  fi
}

get_rhost_ip()
{
  net lookup $1
}

get_rhost_net()
{
  local host=$1
  local num=${2:-2}
  # Use 2nd network interface by default.

  local info_all=$(ssh $host -- ip addr | grep "inet ")
  if [ $? != 0 ]; then
    echo "FAIL: get network info from $host failed."
    exit 1
  fi

#  local info_line=$(echo $info_all | awk -v b=$((num+1)) -F inet \
#                                     '{print $b}')
  echo $info_all | awk -v b=$((num+1)) -F inet \
                  '{print $b}' | sed 's/^[ \t]*//g'
}
