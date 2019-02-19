#!/bin/bash
chk_pkg()
{
# check and install packages.
# usage: chk_pkg pkg1 pkg2 ...

  local rpm_pkg=$*
  local i
  for i in $rpm_pkg
    do
      if rpm -qi $i > /dev/null 2>&1; then
        echo "$i is installed."
      else
        echo "$i isn't installed, now install..."
        yum install -y $i > /dev/null 2>&1;
        if [ $? != 0 ]; then
          echo "Install $i failed, check yum setting and retry."
          exit 1
        fi
      fi
    done
}

chk_cmd()
{
# check and install cmd.
  local cmd=$*
  local i=
  for i in $cmd
    do
      if which $i > /dev/null
      then
        echo "Check $i succeed."
      else
        echo "ERROR: $i is needed."
        exit 1
      fi
    done
}
        
    

chk_off_service()
{
# check if service isn't off, then turn it off.
# chk_off_service host service1 service2 ...
  local host=$1
  shift
  local service=$*
  local i=
  for i in $service
    do
      ssh $host service $i status > /dev/null 2>&1
      if [ $? -eq 0 ]; then
        ssh $host service $i stop > /dev/null 2>&1
        if [ $? != 0 ]; then
          echo "FAIL: stop $i failed."
          exit 1
        fi
      fi
    done
}

chk_on_service()
{
# check if service isn't on, then turn it on.
# chk_on_service host service1 service2 ...
  local host=$1
  shift
  local service=$*
  local i=
  for i in $service
    do
      ssh $host service $i status > /dev/null 2>&1
      if [ $? != 0 ]; then
        ssh $host service $i start > /dev/null 2>&1
        if [ $? != 0 ]; then
          echo "FAIL: start $i failed."
          exit 1
        fi
      fi
    done
}

chk_off_selinux()
{
# turn off selinux on specified host.
# chk_off_selinux host
  local host=$1
  local se_stat=`ssh $1 -- getenforce`
  if [ "$se_stat" == "Enforcing" ]; then
    echo "selinux is enforcing, now set to 0..."
    ssh $host -- "setenforce 0" > /dev/null 2>&1
  fi
  se_stat=`ssh $host -- getenforce`
  if [ "$se_stat" == "Enforcing" ];then
    echo "FAIL: cannot set selinux to 0, exit."
    exit 1
  fi
}

chk_fs()
{
# check if dev is of fs_type
# chk_fs dev fs_type
  local dev=$1
  local fs_type=$2
  if file -sL $dev | grep $fs_type > /dev/null 2>&1; then
    :
  else
    echo "WARNING: Device or file system wrong."
    exit 1
  fi

}

chk_on_rsh()
{
# config and open rsh on rhost for lhost user.
# chk_on_rsh rhost lhost
  local rhost=$1
  local lhost=$2
  timeout 10 rsh $RHOST -- whoami > /dev/null 2>&1
  if [ $? !=0 ]; then
    ssh $rhost "echo -ne 'rsh\nrlogin\nrexec' >> /etc/securetty"
    ssh $rhost "echo $lhost >> /root/.rhosts"
    ssh $rhost which systemctl > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      ssh $rhost systemctl start rsh.socket
      ssh $rhost systemctl start rlogin.socket
    else
      ssh $rhost sed -i '14s/yes/no/' /etc/xinetd.d/rsh
      ssh $rhost sed -i '13s/yes/no/' /etc/xinetd.d/rlogin
      ssh $rhost service xinetd restart
    fi
  else
    echo "rsh already set."
  fi

  local wh=`rsh $rhost -- whoami`
  if [ "$wh" != "root" ]; then
    echo "FAIL: set rsh failed."
    exit 1
  fi

}

chk_cmd()
{
# check if command(s) exists.
  local cmd
  for cmd in $*
    do
      if ! command -v $cmd > /dev/null 2>&1; then
        echo "'$cmd' not found."
      fi
    done
}
