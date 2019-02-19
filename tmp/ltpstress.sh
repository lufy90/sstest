#!/bin/bash
# run ltpstress
# 20180905, by Lufei

. ./net_test.sh
. ./sys_test.sh

download_url="ftp://192.168.45.14/tool/ltp-full-20160920.tar.xz"
wget $download_url
tar_name="ltp-full-20160920.tar.xz"
build=$(arch)

dir_name=${tar_name%%.*}
ltp_ver=${tar_name:9:8}                 # get version
ltp_pre="$(pwd)/ltp-$ltp_ver"           # get configure prefix
ltp_res="$(pwd)/results"                # for results

setup()
{
  tar xf $tar_name
  if [ $? != 0 ]; then
    echo "ERROR: tar failed."
    exit 1
  fi

  local rpm_pkg="gcc rsh rsh-server"
  chk_pkg $rpm_pkg

  cd $dir_name
  ./configure --prefix=$ltp_pre --build=$build
  if [ $? != 0 ]; then
    echo "ERROR: configure failed."
    exit 1
  fi

  make && make install
  if [ $? != 0 ]; then
    echo "ERROR: make failed."
    exit 1
  fi
}

run()
{
  local cmd="gcc exportfs rpc.nfsd"
  chk_cmd $cmd

  [ -f /bin/exportfs ] || ln /usr/sbin/exportfs /bin/
  [ -f /bin/rpc.nfsd ] || ln /usr/sbin/rpc.nfsd /bin/

  local i=0
    while [ -d ${ltp_res}.$i ]
    do
      i=$((i+1))
    done
  ltp_res=${ltp_res}.$i

  mkdir $ltp_res
  cd $ltp_pre

  ./testscripts/ltpstress.sh -d $ltp_res/sar.out.0 \
                             -l $ltp_res/stress.log.0 \
                             -p -q \
                             -t 72 \
                             -S > $ltp_res/stress.out.0 2>&1 &

# for debug.

#  cat runtest/stress.part* > runtest/t0
#  ./runltp -f t0 > $ltp_res/stress.out.0 2>&1 &

}

setup
run
