#!/bin/bash
# stb.sh
# for stability test.


steady()
{
local tlen=$1
local cmd="$2"

sleep $tlen &
local tpid=$!

while [[ $(ps -p $tpid -o comm=) == "sleep" ]]
  do
    $cmd
  done

}

#ntpdate -q asia.pool.ntp.org

sleep 43200

cd /home/testdir/
echo "====================================="
echo "Big files test: wget ftp://192.168.45.185/pub/test0/*"
steady 3600 "wget ftp://192.168.45.185/pub/test0/*"


rm -rf /home/testdir/*

echo "====================================="
echo "Small files test: wget ftp://192.168.45.185/pub/test1/*"
steady 3600 "wget ftp://192.168.45.185/pub/test1/*"

rm -rf /home/testdir/*

echo "====================================="
echo "Big files test: scp 192.168.45.185:/var/ftp/pub/test0/* /root/testdir/"
steady 3600 "scp 192.168.45.185:/var/ftp/pub/test0/* /home/testdir/"

rm -rf /home/testdir/*
echo "====================================="
echo "Small files test: scp 192.168.45.185:/var/ftp/pub/test1/* /root/testdir/"
steady 3600 "scp 192.168.45.185:/var/ftp/pub/test1/* /home/testdir/"
